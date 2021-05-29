from django.urls import path
from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductsListView,
    ProductUpdateView,
)

app_name = 'products'
urlpatterns = [
    path('', ProductsListView.as_view(), name='products-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:id>/update/',
         ProductUpdateView.as_view(), name='product-update'),
    path('<int:id>/delete/',
         ProductDeleteView.as_view(), name='product-delete'),
]
