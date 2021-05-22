from django.urls import path
from .views import (
    CostCreateView,
    CostsListView,
    CostDeleteView,
    CostDetailView,
    CostUpdateView,
)

app_name = 'costs'
urlpatterns = [
    path('', CostsListView.as_view(), name='costs-list'),
    path('create/', CostCreateView.as_view(), name='cost-create'),
    path('<int:id>/', CostDetailView.as_view(), name='cost-detail'),
    path('<int:id>/update/', CostUpdateView.as_view(), name='cost-update'),
    path('<int:id>/delete/', CostDeleteView.as_view(), name='cost-delete'),
]
