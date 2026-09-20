from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryListView, ProductListView, StoreViewSet, ProductDetailView, ProductTrackClickView

router = DefaultRouter()
router.register("stores", StoreViewSet, basename="store")

urlpatterns = router.urls + [
    path("stores/<slug:store_slug>/categories/", CategoryListView.as_view(), name="store-categories"),
    path("stores/<slug:store_slug>/products/", ProductListView.as_view(), name="store-products"),
    path("stores/<slug:store_slug>/products/<int:product_id>/", ProductDetailView.as_view(),
         name="store-product-detail"),
    path("stores/<slug:store_slug>/products/<int:product_id>/track-click/", ProductTrackClickView.as_view(),
         name="store-product-track-click"),

]