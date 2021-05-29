from django.urls import path
from .views import (
    ItemCreateView,
    ItemDeleteView,
    ItemUpdateView,
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
    path('<int:id>/add-item/', ItemCreateView.as_view(),
         name='order-add-item'),
    path('<int:id>/delete-item/<int:item>', ItemDeleteView.as_view(),
         name='order-delete-item'),
    path('<int:id>/update-item/<int:item>', ItemUpdateView.as_view(),
         name='order-update-item'),
    #     path(r'^(?P<id>[0-9]+)$/delete-item/(?P<item>[0-9]+)$',
    #          ItemDeleteView.as_view(), name='order-delete-item'),
    #  path('<int:id>/add-fabric/', OrderDeleteView.as_view(),
    #  name='order-add-fabric'),
]
