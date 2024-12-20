from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    CreateProductView,
    ProductListView,
    DeleteProductView,
    UpdateProductView,
    ProductDetailView,
    AddToCartView,
    ViewCartView,
    DeleteFromCartView,
    CommentView, LikeProductView, RatingView,LikedProductsView,PurchaseView,OrderHistoryView
)

urlpatterns = [
    path('create_product/', CreateProductView.as_view(), name='create_product'),
    path('get_products/', ProductListView.as_view(), name='get_products'),
    path('delete/<int:product_id>/', DeleteProductView.as_view(), name='delete_product'),
    path('update/<int:product_id>/', UpdateProductView.as_view(), name='update_product'), 
    path('get_product/<int:id>/', ProductDetailView.as_view(), name='get_product'), # Endpoint for getting a single product by ID
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('view_cart/', ViewCartView.as_view(), name='view_cart'),
    path('cart/delete/<int:product_id>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('products/<int:product_id>/comments/', CommentView.as_view(), name='product_comments'),
    path('products/<int:product_id>/like/', LikeProductView.as_view(), name='like_product'),
    path('liked-products/', LikedProductsView.as_view(), name='liked-products'),
    path('products/<int:product_id>/ratings/', RatingView.as_view(), name='product_ratings'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



