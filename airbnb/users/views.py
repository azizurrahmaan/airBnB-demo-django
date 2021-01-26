from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import SignUpForm, UpdateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from django.db.models import Q

def landing(request):
    """
    Redirects users based on authentication
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard')
        return super(SignUpView, self).get(request, *args, **kwargs)


class UpdateProfile(LoginRequiredMixin, FormView):
    login_url = 'login'
    form_class = UpdateProfileForm
    success_url = "/"
    template_name = 'users/profile.html'

    def form_valid(self, form):
        form.save(self.request)
        return super(UpdateProfile, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UpdateProfile, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class Chats(LoginRequiredMixin, TemplateView):
    template_name = 'users/chats.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(Chats, self).get(request, *args, **kwargs)
        return Http404

    def get_context_data(self, **kwargs):
        chats = Chat.objects.filter(Q(owner=self.request.user) | Q(participants__in=[self.request.user]))
        context = {"chats": chats}
        return context