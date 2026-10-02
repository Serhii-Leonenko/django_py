from django.urls import path, include

from users.views import UserRegisterView, UserActivationView

app_name = "registration"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name='register'),
    path("", include("django.contrib.auth.urls")),
    path("activate/<str:uid>/<str:token>/", UserActivationView.as_view(), name="activate")
]
