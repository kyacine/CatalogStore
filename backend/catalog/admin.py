from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, Store, ProductInquiry


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "whatsapp_number", "is_active", "category_count", "product_count")
    list_editable = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    @admin.display(description="Catégories")
    def category_count(self, obj):
        return obj.categories.count()

    @admin.display(description="Produits")
    def product_count(self, obj):
        return obj.products.count()

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ("primary_color", "accent_color"):
            kwargs["widget"] = forms.TextInput(attrs={"type": "color"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "store", "order", "product_count")
    list_editable = ("order",)
    list_filter = ("store",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    autocomplete_fields = ("store",)

    @admin.display(description="Nb de produits")
    def product_count(self, obj):
        return obj.products.count()


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "order", "preview")
    readonly_fields = ("preview",)

    @admin.display(description="Aperçu")
    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "name", "store", "category", "price", "is_available", "inquiry_count", "updated_at")
    list_display_links = ("thumbnail", "name")
    list_editable = ("is_available",)
    list_filter = ("store", "category", "is_available")
    search_fields = ("name", "description")
    autocomplete_fields = ("store", "category")
    fields = ("store", "name", "category", "price", "description", "is_available")
    inlines = [ProductImageInline]

    @admin.display(description="Photo")
    def thumbnail(self, obj):
        first_image = obj.images.first()
        if first_image:
            return format_html(
                '<img src="{}" style="height:45px;width:45px;object-fit:cover;border-radius:6px;" />',
                first_image.image.url,
            )
        return "—"

    @admin.display(description="Demandes")
    def inquiry_count(self, obj):
        return obj.inquiries.count()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limits the "Category" dropdown to categories from the store already
        # selected, to avoid mismatches once several stores exist.
        if db_field.name == "category":
            store_id = request.GET.get("store") or request.POST.get("store")
            if store_id:
                kwargs["queryset"] = Category.objects.filter(store_id=store_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = ("product", "created_at")
    list_filter = ("product__store", "created_at")
    date_hierarchy = "created_at"
    search_fields = ("product__name",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.site_header = "Gestion du catalogue"
admin.site.site_title = "Catalogue"
admin.site.index_title = "Ajouter et modifier les boutiques et produits"