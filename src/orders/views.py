import io
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from .models import Order, Item, Fabric, Payment
from .forms import (
    OrderModelForm,
    ItemModelForm,
    ItemUpdateForm,
    FabricModelForm,
    FabricUpdateForm,
    PaymentModelForm,
    PaymentUpdateForm,
)
from .utils import PDFReport
import datetime


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

    # ! TENGO QUE MOSTRAR SUBTOTAL Y EL DESCUENTO
    # ! EL PDF TIENE QUE TENER LOS ITEMS, HAY QUE PASÁRSELOS A LA VIEW

    order = get_object_or_404(Order, id=id)
    items = order.items.all()
    fabrics = order.fabrics.all()
    payments = order.payments.all()
    balances = order.get_balances(items, fabrics, payments)
    context = {
        "order": order,
        'items': items,
        'fabrics': fabrics,
        'payments': payments,
        'items_total': balances['items_total'],
        'items_prices': balances['items_prices'],
        'fabrics_total': balances['fabrics_total'],
        'total': balances['total'],
        'payments_total': balances['payments_total'],
        'left_balance': balances['left_balance'],
        'net_worth': balances['net_worth'],
    }
    return render(request, 'orders/order_detail.html', context)


def generate_pdf_report(request, id, *args, **kwargs):

    order = get_object_or_404(Order, id=id)

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    today = datetime.datetime.today()
    fifteen_days = datetime.timedelta(15)
    expiration_date = today + fifteen_days
    output = "{:%d/%m/%Y}"
    today = output.format(today)
    expiration_date = output.format(expiration_date)

    pdf = PDFReport(
        buffer,
        title='Presupuesto',
        expiration_date=expiration_date,
        id=order.id,
        date=today,
        customer_info={
            'first': order.customer_first_name,
            'last': order.customer_last_name,
            'tel': order.customer_tel,
            'email': order.customer_email,
            'city': order.customer_city,
            'zip_code': order.customer_zip_code,
            'state': order.customer_state,
        },
        order_items=[
            ["Confección 1", "1", "5000", "5000"],
            ["Confección 2", "2", "2500", "5000"],
            ["Confección 3", "5", "1000", "5000"],
        ],
        results={
            'subtotal': 15000,
            'discount_percentage': 10,
            'discount_amount': 1500,
            'total': 13500,
        })
    pdf.create_pdf()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


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
        return reverse('home')


class ItemCreateView(CreateView):
    template_name = 'orders/item_create.html'
    form_class = ItemModelForm

    def get_initial(self, **kwargs):
        initial = super(ItemCreateView, self).get_initial(**kwargs)
        id_ = self.kwargs.get("id")
        order = Order.objects.get(id=id_)
        initial['order'] = order
        return initial

    def get_success_url(self):
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})


class ItemDeleteView(DeleteView):
    template_name = 'orders/item_delete.html'

    def get_object(self):
        item_id_ = self.kwargs.get("item")
        return get_object_or_404(Item, id=item_id_)

    def get_success_url(self):
        print(self.object.order.id)
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})


class ItemUpdateView(UpdateView):
    template_name = 'orders/item_update.html'
    form_class = ItemUpdateForm

    def get_object(self):
        item_id_ = self.kwargs.get("item")
        return get_object_or_404(Item, id=item_id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})


class FabricCreateView(CreateView):
    template_name = 'orders/fabric_create.html'
    form_class = FabricModelForm

    def get_initial(self, **kwargs):
        initial = super(FabricCreateView, self).get_initial(**kwargs)
        id_ = self.kwargs.get("id")
        order = Order.objects.get(id=id_)
        initial['order'] = order
        return initial

    def get_success_url(self):
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})


class FabricDeleteView(DeleteView):
    template_name = 'orders/fabric_delete.html'

    def get_object(self):
        fabric_id_ = self.kwargs.get("fabric")
        return get_object_or_404(Fabric, id=fabric_id_)

    def get_success_url(self):
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})


class FabricUpdateView(UpdateView):
    template_name = 'orders/fabric_update.html'
    form_class = FabricUpdateForm

    def get_object(self):
        fabric_id_ = self.kwargs.get("fabric")
        return get_object_or_404(Fabric, id=fabric_id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})


class PaymentCreateView(CreateView):
    template_name = 'orders/payment_create.html'
    form_class = PaymentModelForm

    def get_initial(self, **kwargs):
        initial = super(PaymentCreateView, self).get_initial(**kwargs)
        id_ = self.kwargs.get("id")
        order = Order.objects.get(id=id_)
        initial['order'] = order
        return initial

    def get_success_url(self):
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})


class PaymentDeleteView(DeleteView):
    template_name = 'orders/payment_delete.html'

    def get_object(self):
        payment_id_ = self.kwargs.get("payment")
        return get_object_or_404(Payment, id=payment_id_)

    def get_success_url(self):
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})


class PaymentUpdateView(UpdateView):
    template_name = 'orders/payment_update.html'
    form_class = PaymentUpdateForm

    def get_object(self):
        payment_id_ = self.kwargs.get("payment")
        return get_object_or_404(Payment, id=payment_id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:order-detail',
                       kwargs={'id': self.object.order.id})
