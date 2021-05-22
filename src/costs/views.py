from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from .models import Cost
from .forms import CostModelForm


class CostCreateView(CreateView):
    template_name = 'costs/cost_create.html'
    form_class = CostModelForm
    queryset = Cost.objects.all()  # <blog>/<modelname>_list.html
    # success_url = '/'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return '/'


class CostsListView(ListView):
    template_name = 'costs/costs_list.html'
    queryset = Cost.objects.all()  # <blog>/<modelname>_list.html


class CostDetailView(DetailView):
    template_name = 'costs/cost_detail.html'
    # queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Cost, id=id_)


class CostUpdateView(UpdateView):
    template_name = 'costs/cost_create.html'
    form_class = CostModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Cost, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class CostDeleteView(DeleteView):
    template_name = 'costs/cost_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Cost, id=id_)

    def get_success_url(self):
        return reverse('costs:costs-list')
