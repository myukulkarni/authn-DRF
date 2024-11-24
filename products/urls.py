<<<<<<< HEAD
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
    DeleteFromCartView
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
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




    
=======
from django.urls import path
from . import views

urlpatterns = [
    path('create_product/', views.create_product, name='create_product'),
    path('get_products/', views.get_products, name='get_products'),
]
>>>>>>> 0da9d9919c2e0d416f821a2b0df46d12a2b74e28
