from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from .models import Order  # , Item
from .forms import OrderModelForm, ItemModelForm


class OrderCreateView(CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderModelForm
    queryset = Order.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class OrdersListView(ListView):
    template_name = 'orders/orders_list.html'
    queryset = Order.objects.all()  # <blog>/<modelname>_list.html


class OrderDetailView(DetailView):
    template_name = 'orders/order_detail.html'
    # queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Order, id=id_)


def get_order_detail_view(request, id, *args, **kwargs):
    order = get_object_or_404(Order, id=id)
    items = order.items.all()
    print(items)
    fabrics = order.fabrics.all()
    payments = order.payments.all()
    balances = order.get_balances(items, fabrics, payments)
    context = {
        "order": order,
        'items': items,
        'fabrics': fabrics,
        'items_total': balances['items_total'],
        'fabrics_total': balances['fabrics_total'],
        'total': balances['total'],
        'payments_total': balances['payments_total'],
        'left_balance': balances['left_balance'],
    }
    return render(request, 'orders/order_detail.html', context)


class OrderUpdateView(UpdateView):
    template_name = 'orders/order_create.html'
    form_class = OrderModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Order, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    template_name = 'orders/order_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Order, id=id_)

    def get_success_url(self):
        return reverse('orders:orders-list')


class ItemCreateView(CreateView):
    template_name = 'orders/item_create.html'
    form_class = ItemModelForm

    def get_initial(self, *args, **kwargs):
        initial = super(ItemCreateView, self).get_initial(**kwargs)
        id_ = self.kwargs.get("id")
        order = Order.objects.get(id=id_)
        initial['order'] = order
        return initial
