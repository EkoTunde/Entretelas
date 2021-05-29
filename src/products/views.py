from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from .forms import ProductModelForm
from .models import Product


class ProductCreateView(CreateView):
    template_name = 'products/product_create.html'
    form_class = ProductModelForm
    queryset = Product.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ProductsListView(ListView):
    template_name = 'products/products_list.html'
    queryset = Product.objects.all()


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Product, id=id_)


class ProductUpdateView(UpdateView):
    template_name = 'products/product_create.html'
    form_class = ProductModelForm

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Product, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    template_name = 'products/product_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Product, id=id_)

    def get_success_url(self):
        return reverse('products:products-list')
