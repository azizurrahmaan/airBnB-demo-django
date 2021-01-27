from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Message, Chat

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "username", "email","password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        self.initial['username'] = self.user.username
        self.initial['email'] = self.user.email
        self.initial['first_name'] = self.user.first_name
        self.initial['last_name'] = self.user.last_name

    def save(self, request):
        user = request.user
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        return user


class CreateMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('chat', 'message')
        
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateMessageForm, self).__init__(*args, **kwargs)
    
    def save(self):
        message = Message(**self.cleaned_data)
        message.sender = self.user
        message.save()
        return message

class CreateChatForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ('topic',)
        
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.participants = kwargs.pop('participants')
        super(CreateChatForm, self).__init__(*args, **kwargs)
    
    def save(self):
        chat = Chat(**self.cleaned_data)
        chat.owner = self.user
        chat.save()
        chat.participants.set(self.participants)
        return chat