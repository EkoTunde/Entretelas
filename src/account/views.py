from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView
from .models import Account
from .forms import AccountModelForm


class AccountObjectMixin(object):
    model = Account

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class AccountDetailView(DetailView):
    template_name = 'account/account_detail.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Account, id=id_)


class AccountUpdateView(AccountObjectMixin, View):
    template_name = 'account/account_update.html'

    def get(self, request, id=None, success=0, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AccountModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        success = False
        if request.GET:
            success = request.GET.get('success', False)
            context['success'] = success
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AccountModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            context['success'] = True
        return render(request, self.template_name, context)
