from django.urls import path
from .views import AccountUpdateView


app_name = 'account'
urlpatterns = [

    # Order
    path('<int:id>/', AccountUpdateView.as_view(), name='update'),
    # path('create/', OrderCreateView.as_view(), name='order-create'),
    # path('<int:id>/', get_order_detail_view, name='order-detail'),
    # path('<int:id>/update/', OrderUpdateView.as_view(), name='order-update'),
    # path('<int:id>/delete/', OrderDeleteView.as_view(), name='order-delete'),
]
