from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from core.mixins import BootstrapFormMixin

User = get_user_model()


class UserRegisterForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


class UserLoginForm(BootstrapFormMixin, AuthenticationForm):
    pass
