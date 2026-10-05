from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from users.forms import UserRegisterForm
from users.services.user_service import get_user_service


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("registration:login")

    def form_valid(self, form):
        url = self.request.build_absolute_uri("/")

        user_service = get_user_service()
        user_service.register_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
            url=url
        )

        messages.success(self.request, "User created successfully, check your email to activate your account")

        return super().form_valid(form)


class UserActivationView(View):
    def get(self, request: HttpRequest, uid: str, token:str):
        user_service = get_user_service()
        user_service.activate_user(uid, token)

        return redirect("messenger:home")
