import io
from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import cm
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
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


def some_view(request, *args, **kwargs):
    template_path = "orders/order_pdf.html"
    id_ = kwargs.get("id")
    order = get_object_or_404(Order, id=id_)
    items = order.items.all()
    fabrics = order.fabrics.all()
    payments = order.payments.all()
    balances = order.get_balances(items, fabrics, payments)
    context = {
        'order': order,
        'total': balances['total'],
        'payments_total': balances['payments_total'],
        'left_balance': balances['left_balance'],
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

    # # Create a file-like buffer to receive PDF data.
    # buffer = io.BytesIO()

    # # Create the PDF object, using the buffer as its "file."
    # c = canvas.Canvas(buffer, pagesize=A4)

    # MAX_WIDTH = 595.2755905511812
    # HALF_WIDTH = MAX_WIDTH / 2
    # MAX_LENGTH = 841.8897637795277
    # HALF_LENGTH = MAX_LENGTH / 2

    # # HEADER
    # c.setFillColorRGB(0, 0, 0)
    # c.rect(10, MAX_LENGTH-20, HALF_WIDTH-65, 10, stroke=0, fill=1)
    # c.rect(MAX_WIDTH-10, MAX_LENGTH-20, -(HALF_WIDTH-65), 10, stroke=0, fill=1)
    # c.setFillColorRGB(255, 255, 255)
    # # c.rect(MAX_WIDTH/2-55, MAX_LENGTH-20, 55*2, 10, stroke=0, fill=1)

    # c.setFont("Helvetica", 12)

    # c.setFillColorRGB(0, 0, 0)
    # c.drawCentredString(MAX_WIDTH/2, MAX_LENGTH-19.5, "PRESUPUESTO")
    # # textobject = c.beginText()
    # # textobject.setTextOrigin(MAX_WIDTH/2, MAX_LENGTH-10)
    # # textobject.setFont("Helvetica", 14)
    # # textobject.textLines('PRESUPUESTO')
    # # c.drawText(textobject)

    # # define a large font

    # # Close the PDF object cleanly, and we're done.
    # c.showPage()
    # c.save()

    # # FileResponse sets the Content-Disposition header so that browsers
    # # present the option to save the file.
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


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
