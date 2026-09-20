import unicodedata

from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, Store, ProductInquiry
from .serializers import CategorySerializer, ProductSerializer, StoreSerializer


def strip_accents(text):
    """Retire les accents pour permettre une recherche insensible aux accents,
    ex: "deter" retrouve "détergent"."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)
    ).lower()


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """Fiche publique d'une boutique (nom, tagline, adresse, numéro WhatsApp, logo)."""

    queryset = Store.objects.filter(is_active=True)
    serializer_class = StoreSerializer
    lookup_field = "slug"

    def get_serializer_context(self):
        return {"request": self.request}


class StoreScopedMixin:
    """Récupère la boutique active à partir du slug dans l'URL, ou 404."""

    def get_store(self):
        return get_object_or_404(Store, slug=self.kwargs["store_slug"], is_active=True)


class CategoryListView(StoreScopedMixin, generics.ListAPIView):
    """Liste des catégories d'une boutique, pour construire les filtres du catalogue."""

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(store=self.get_store())


class ProductPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 50


class ProductListView(StoreScopedMixin, generics.ListAPIView):
    """
    Catalogue public d'une boutique : ne renvoie que les produits disponibles.
    Filtrable par catégorie via ?category=<slug> et par recherche via ?search=<texte>.
    """

    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = (
            Product.objects.filter(store=self.get_store(), is_available=True)
            .select_related("category", "store")
            .prefetch_related("images")
        )
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        search = self.request.query_params.get("search")
        if search:
            needle = strip_accents(search)
            queryset = [
                product for product in queryset
                if needle in strip_accents(product.name)
                   or needle in strip_accents(product.description or "")
            ]

        return queryset

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetailView(StoreScopedMixin, generics.RetrieveAPIView):
    """Fiche détaillée d'un produit (toutes ses photos, description complète)."""

    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_queryset(self):
        return Product.objects.filter(
            store=self.get_store(), is_available=True
        ).select_related("category", "store").prefetch_related("images")

    def get_serializer_context(self):
        return {"request": self.request}


class ProductTrackClickView(StoreScopedMixin, APIView):
    """Enregistre un clic sur le bouton WhatsApp d'un produit. Ne renvoie aucune donnée."""

    def post(self, request, store_slug, product_id):
        product = get_object_or_404(Product, store=self.get_store(), id=product_id)
        ProductInquiry.objects.create(product=product)
        return Response(status=204)