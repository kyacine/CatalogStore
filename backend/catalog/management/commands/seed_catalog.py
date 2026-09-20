from django.core.management.base import BaseCommand

from catalog.models import Category, Product, Store

STARTER_CATEGORIES = [
    ("Ménage", 1),
    ("Parfum", 2),
    ("Encens", 3),
    ("Alimentaire", 4),
    ("Beauté", 5),
    ("Autre", 99),
]


class Command(BaseCommand):
    help = "Crée une boutique de démonstration avec des catégories de départ, si la base est vide."

    def add_arguments(self, parser):
        parser.add_argument(
            "--store-name",
            default="Ma Boutique",
            help="Nom de la boutique à créer si aucune n'existe encore.",
        )
        parser.add_argument(
            "--whatsapp-number",
            default="33600000000",
            help="Numéro WhatsApp (format international, sans le +) de la boutique de démo.",
        )

    def handle(self, *args, **options):
        store, store_created = Store.objects.get_or_create(
            name=options["store_name"],
            defaults={"whatsapp_number": options["whatsapp_number"]},
        )
        if store_created:
            self.stdout.write(self.style.SUCCESS(f"Boutique '{store}' créée."))
        else:
            self.stdout.write(f"Boutique '{store}' déjà existante, réutilisée.")

        created_categories = 0
        for name, order in STARTER_CATEGORIES:
            _, created = Category.objects.get_or_create(
                store=store, name=name, defaults={"order": order}
            )
            created_categories += int(created)

        if not store.products.exists():
            menage = Category.objects.get(store=store, name="Ménage")
            Product.objects.create(
                store=store,
                name="Exemple : Savon liquide 500ml",
                category=menage,
                description="Ceci est un produit d'exemple, à modifier ou supprimer dans l'admin.",
                price="2.50",
                is_available=True,
            )
            self.stdout.write(self.style.SUCCESS("Produit d'exemple créé."))

        self.stdout.write(
            self.style.SUCCESS(
                f"{created_categories} nouvelle(s) catégorie(s) créée(s) pour '{store}' "
                f"(slug: {store.slug})."
            )
        )