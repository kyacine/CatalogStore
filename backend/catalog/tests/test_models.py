from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog.models import Category, Product, Store, validate_image_size


class ProductCategoryStoreConsistencyTests(TestCase):
    """Un produit ne doit jamais pouvoir être associé à une catégorie
    appartenant à une autre boutique."""

    def setUp(self):
        self.store_a = Store.objects.create(name="Boutique A", whatsapp_number="33600000001")
        self.store_b = Store.objects.create(name="Boutique B", whatsapp_number="33600000002")
        self.category_b = Category.objects.create(store=self.store_b, name="Catégorie B")

    def test_category_from_another_store_is_rejected(self):
        product = Product(
            store=self.store_a,
            category=self.category_b,
            name="Produit test",
            price="10.00",
        )
        with self.assertRaises(ValidationError):
            product.clean()

    def test_category_from_the_same_store_is_accepted(self):
        category_a = Category.objects.create(store=self.store_a, name="Catégorie A")
        product = Product(
            store=self.store_a,
            category=category_a,
            name="Produit test",
            price="10.00",
        )
        # Ne doit lever aucune exception.
        product.clean()

    def test_product_without_category_is_accepted(self):
        product = Product(store=self.store_a, name="Produit sans catégorie", price="10.00")
        # Une catégorie est facultative (blank=True, null=True) : pas d'erreur attendue.
        product.clean()


class StoreSlugTests(TestCase):
    """Le slug d'une boutique est généré une seule fois, à la création,
    et ne doit jamais changer même si le nom change ensuite."""

    def test_slug_is_generated_on_creation(self):
        store = Store.objects.create(name="Ma Belle Boutique", whatsapp_number="33600000000")
        self.assertEqual(store.slug, "ma-belle-boutique")

    def test_slug_does_not_change_when_name_changes(self):
        store = Store.objects.create(name="Nom Initial", whatsapp_number="33600000000")
        original_slug = store.slug

        store.name = "Nom Complètement Différent"
        store.save()

        store.refresh_from_db()
        self.assertEqual(store.slug, original_slug)


class ImageSizeValidationTests(TestCase):
    """La taille des photos uploadées est limitée pour protéger le quota Cloudinary."""

    def test_image_under_the_limit_is_accepted(self):
        small_file = type("FakeFile", (), {"size": 1 * 1024 * 1024})()  # 1 Mo
        # Ne doit lever aucune exception.
        validate_image_size(small_file)

    def test_image_over_the_limit_is_rejected(self):
        big_file = type("FakeFile", (), {"size": 6 * 1024 * 1024})()  # 6 Mo
        with self.assertRaises(ValidationError):
            validate_image_size(big_file)