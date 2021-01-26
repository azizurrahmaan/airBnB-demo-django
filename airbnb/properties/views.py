from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import AddPropertyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, TemplateView
from properties.models import Property
from django.db.models import Q

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'properties/dashboard.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(Dashboard, self).get(request, *args, **kwargs)
        return Http404

    def get_context_data(self, **kwargs):
        properties = Property.objects.filter(~Q(owner=self.request.user))
        context = {"properties": properties}
        return context


class MyProperties(LoginRequiredMixin, TemplateView):
    template_name = 'properties/my_properties.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(MyProperties, self).get(request, *args, **kwargs)
        return Http404

    def get_context_data(self, **kwargs):
        properties = Property.objects.filter(Q(owner=self.request.user))
        context = {"properties": properties}
        return context


class AddProperty(LoginRequiredMixin, FormView):
    login_url = 'login'
    form_class = AddPropertyForm
    success_url = "/my-properties"
    template_name = 'properties/add_properties.html'

    def form_valid(self, form):
        form.save(self.request)
        return super(AddProperty, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AddProperty, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs