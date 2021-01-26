from django.urls import path, include
from users.views import landing, SignUpView, UpdateProfile, Chats

urlpatterns = [
    path('', landing, name='landing'),
    # Users Urls
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", UpdateProfile.as_view(), name="profile"),
    # Chats Urls
    path("chats/", Chats.as_view(), name="chats"),
]