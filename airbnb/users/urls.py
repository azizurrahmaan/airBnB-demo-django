from django.urls import path, include
from users.views import landing, SignUpView, UpdateProfile

urlpatterns = [
    path('', landing, name='landing'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", UpdateProfile.as_view(), name="profile"),

]