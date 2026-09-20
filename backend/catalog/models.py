from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


MAX_IMAGE_SIZE_MB = 5


def validate_image_size(image):
    """Empêche l'upload de photos trop lourdes (protège le quota Cloudinary)."""
    limit_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
    if image.size > limit_bytes:
        raise ValidationError(f"L'image ne doit pas dépasser {MAX_IMAGE_SIZE_MB} Mo.")

class Store(models.Model):
    """A shop/merchant. Each store has its own catalogue and its own
    WhatsApp number for receiving orders"""

    name = models.CharField("Nom de la boutique", max_length=150)
    slug = models.SlugField("Slug", max_length=160, unique=True, blank=True)
    tagline = models.CharField("Phrase d'accroche", max_length=200, blank=True)
    whatsapp_number = models.CharField(
        "Numéro WhatsApp",
        max_length=20,
        help_text="Format international sans le \"+\" ni espaces, ex: 33612345678.",
    )
    address = models.CharField('Adresse', max_length=255, blank=True)
    logo = models.ImageField("Logo", upload_to="stores/", blank=True, null=True,
                             validators=[validate_image_size])
    is_active = models.BooleanField("Boutique active", default=True)
    created_at = models.DateTimeField("Créée le", auto_now_add=True)
    currency = models.CharField(
        "Devise",
        max_length=10,
        default="€",
        help_text="Symbole ou code affiché à côté des prix, ex: €, FCFA, $.",
    )
    primary_color = models.CharField(
        "Couleur principale",
        max_length=7,
        default="#2f4b3c",
        help_text="Couleur du bandeau d'en-tête, format hexadécimal (ex: #2f4b3c).",
    )
    accent_color = models.CharField(
        "Couleur d'accent",
        max_length=7,
        default="#e2a13a",
        help_text="Couleur des prix et éléments mis en avant, format hexadécimal (ex: #e2a13a).",
    )

    class Meta:
        verbose_name = "Boutique"
        verbose_name_plural = "Boutiques"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """A product family, e.g. Household, Perfume, Incense, Groceries"""

    store = models.ForeignKey(Store, verbose_name="Boutique", related_name="categories", on_delete=models.CASCADE)
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField("Slug", max_length=110, blank=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["order", "name"]
        unique_together = [("store", "slug")]

    def __str__(self):
        return f"{self.name} ({self.store.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """A catalogue item shown on the public storefront."""

    store = models.ForeignKey(Store, verbose_name="Boutique", related_name="products", on_delete=models.CASCADE)
    name = models.CharField("Nom du produit", max_length=150)
    category = models.ForeignKey(
        Category, verbose_name="Catégorie", related_name="products",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    description = models.TextField("Description", blank=True)
    price = models.DecimalField("Prix", max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField("Disponible", default=True)
    created_at = models.DateTimeField("Ajouté le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def clean(self):
        # A product's category must belong to the same store as the product
        # itself - guards against mismatches once several stores exist.
        if self.category_id and self.category.store_id != self.store_id:
            raise ValidationError({"category": "Cette catégorie n'appartient pas à la boutique sélectionnée."})


class ProductImage(models.Model):
    """A product photo. The image with the lowest `order` is used as the
    primary photo shown in the catalogue grid."""

    product = models.ForeignKey(Product, verbose_name="Produit", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField("Photo", upload_to="products/", validators=[validate_image_size])
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Photo produit"
        verbose_name_plural = "Photos produit"
        ordering = ["order", "id"]

    def __str__(self):
        return f"Photo #{self.order} de {self.product.name}"


class ProductInquiry(models.Model):
    """
    Records every click on a "Request"/"Order" button to track
    which products generate the most interest. No personal data
    is stored - just a timestamped counter per product.
    """

    product = models.ForeignKey(
        Product, verbose_name="Produit", related_name="inquiries", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField("Demandé le", auto_now_add=True)

    class Meta:
        verbose_name = "Demande WhatsApp"
        verbose_name_plural = "Demandes WhatsApp"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Demande pour {self.product.name} le {self.created_at:%d/%m/%Y %H:%M}"