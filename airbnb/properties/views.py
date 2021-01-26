from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import AddPropertyForm, EditPropertyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
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
        properties_count = Property.objects.filter(Q(owner=self.request.user)).count()
        context = {"properties_count": properties_count}
        return context


class Properties(TemplateView):
    template_name = 'properties/properties.html'
    # login_url = 'login'

    def get(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        return super(Properties, self).get(request, *args, **kwargs)
        # return Http404

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            properties = Property.objects.filter(~Q(owner=self.request.user))
        else:
            properties = Property.objects.all()
        
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
    success_url = "/properties/my"
    template_name = 'properties/add_properties.html'

    def form_valid(self, form):
        form.save(self.request)
        return super(AddProperty, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AddProperty, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EditProperty(LoginRequiredMixin, UpdateView):
    login_url = 'account_login'
    model = Property
    form_class = EditPropertyForm
    success_url = "/"
    template_name = 'properties/edit_property.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(EditProperty, self).get(request, *args, **kwargs)
        return Http404

    def get_object(self, queryset=None):
        property = Property.objects.get(pk=self.kwargs['pk'])
        return property


class PropertyDetail(TemplateView):
    template_name = 'properties/property_details.html'
    # login_url = 'login'

    def get(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        return super(PropertyDetail, self).get(request, *args, **kwargs)
        # return Http404

    def get_context_data(self, **kwargs):
        property = Property.objects.filter(pk=self.kwargs['pk']).first()
        context = {"property": property}
        return context