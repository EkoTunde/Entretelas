from django.urls import path
from .views import (
    OrderCreateView,
    OrdersListView,
    OrderDeleteView,
    # OrderDetailView,
    OrderUpdateView,
    get_order_detail_view,
)

app_name = 'orders'
urlpatterns = [
    path('', OrdersListView.as_view(), name='orders-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:id>/', get_order_detail_view, name='order-detail'),
    path('<int:id>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('<int:id>/delete/', OrderDeleteView.as_view(), name='order-delete'),
]
