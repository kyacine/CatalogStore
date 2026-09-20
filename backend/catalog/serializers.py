from rest_framework import serializers

from .models import Category, Product, ProductImage, Store


class StoreSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ["id", "name", "slug", "tagline", "address", "whatsapp_number", "logo_url", "currency",
                  "primary_color", "accent_color"]

    def get_logo_url(self, obj):
        if not obj.logo:
            return None
        request = self.context.get("request")
        url = obj.logo.url
        return request.build_absolute_uri(url) if request else url


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "order"]


class ProductImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "url", "order"]

    def get_url(self, obj):
        request = self.context.get("request")
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    # Dénormalisé depuis la boutique : évite un second appel API juste pour
    # construire le lien WhatsApp ou la monnaie côté frontend.
    whatsapp_number = serializers.CharField(source="store.whatsapp_number", read_only=True)
    currency = serializers.CharField(source="store.currency", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "description", "price",
            "image_url", "images", "category", "whatsapp_number", "is_available", "currency",
        ]

    def get_image_url(self, obj):
        """Photo principale (la première par ordre), pour l'affichage en grille."""
        first_image = obj.images.first()
        if not first_image:
            return None
        request = self.context.get("request")
        url = first_image.image.url
        return request.build_absolute_uri(url) if request else url