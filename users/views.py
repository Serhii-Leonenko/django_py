from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from users.forms import UserRegisterForm
from users.services.user_activation_token_service import activation_token_service
from users.services.user_service import UserService


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    user_service = UserService(token_service=activation_token_service)
    success_url = reverse_lazy("registration:login")

    def form_valid(self, form):
        url = self.request.build_absolute_uri("/")

        self.user_service.register_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
            url=url
        )

        messages.success(self.request, "User created successfully, check your email to activate your account")

        return super().form_valid(form)


class UserActivationView(View):
    def get(self, request, uid, token):
        print(uid, token)
        print("we need to activate the user")
