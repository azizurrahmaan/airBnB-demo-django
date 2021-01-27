from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import SignUpForm, UpdateProfileForm, CreateMessageForm, CreateChatForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from django.db.models import Q
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

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


@login_required
def get_messages(request, chat_id):
    chat = Chat.objects.filter(pk=chat_id).first()
    if not chat:
        data = {"errors": "Chat object does not exist."}
    else:
        if chat.owner == request.user or chat.participants.filter(id=request.user.id).exists():
            data = list(Message.objects.filter(chat=chat).order_by('created_on').values('sender__pk', 'sender__first_name', 'sender__last_name', 'message', 'created_on'))
            return JsonResponse(data, safe=False)
        else:
            data = {"errors": "You don't have permission to read the Chat."}
    return JsonResponse(data)


@login_required
def send_message(request):
    chat = Chat.objects.filter(pk=request.POST.get('chat_id')).first()
    if not chat:
        data = {"errors": "Chat object does not exist."}
    else:
        if chat.owner == request.user or chat.participants.filter(id=request.user.id).exists():
            form = CreateMessageForm(request.POST, user=request.user)
            if form.is_valid():
                message = form.save()
                data = model_to_dict(message)
            else:
                data = form.errors
            return JsonResponse(data, safe=False)
        else:
            data = {"errors": "You don't have permission to send message to this Chat."}
    return JsonResponse(data)


@login_required
def create_chat(request):
    chat = Chat.objects.filter(owner=request.user, participants__in=[request.POST['participants']]).first()
    if not chat:
        form = CreateChatForm(request.POST, user=request.user, participants=request.POST['participants'])
        if form.is_valid():
            chat = form.save()
        else:
            data = form.errors
            return JsonResponse(data)
    return redirect(reverse("chats") + "?open_chat=" + str(chat.id))