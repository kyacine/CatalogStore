import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Crée un superutilisateur à partir de variables d'environnement, mais
    uniquement s'il n'en existe pas déjà un. Pensée pour tourner à chaque
    déploiement (dans la commande de build), sans jamais planter sur les
    déploiements suivants une fois le compte déjà créé.
    """

    help = "Crée un superutilisateur depuis les variables d'environnement, si aucun n'existe."

    def handle(self, *args, **options):
        User = get_user_model()

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Un superutilisateur existe déjà, rien à faire.")
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD non définies, "
                "aucun superutilisateur créé."
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superutilisateur '{username}' créé."))