import logging
from functools import cache

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from users.models import Profile
from users.services.user_activation_token_service import UserActivationTokenService, activation_token_service
from users.services.user_email_service import UserEmailService, get_user_email_service

logger = logging.getLogger(__name__)

User = get_user_model()


class UserServiceError(Exception):
    pass


class ActivationTokenError(UserServiceError):
    pass


class UserService:
    DEFAULT_INACTIVE_USER_GROUP = 'InactiveUser'
    DEFAULT_ACTIVE_USER_GROUP = 'User'

    def __init__(self, token_service: UserActivationTokenService, email_service: UserEmailService):
        self._token_service = token_service
        self._email_service = email_service

    def _get_uid(self, user: User):
        return urlsafe_base64_encode(str(user.pk).encode())

    def _decode_uid(self, uid: str):
        return urlsafe_base64_decode(uid).decode()

    def _get_activation_link(self, url: str, user: User):
        uid = self._get_uid(user)
        token = self._token_service.make_token(user)

        return f"{url}users/activate/{uid}/{token}/"

    def register_user(self, username: str, email: str, password: str, url: str) -> User:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=True
            )
            user.groups.add(Group.objects.get(name=self.DEFAULT_INACTIVE_USER_GROUP))
            Profile.objects.create(user=user)
            activation_link = self._get_activation_link(url, user)
            self._email_service.send_activation_email(
                username=username,
                email=email,
                activation_link=activation_link
            )

        return user

    def activate_user(self, uid: str, activation_token: str):
        user = get_object_or_404(User, pk=self._decode_uid(uid))

        try:
            token_verified = self._token_service.check_token(user, activation_token)
        except Exception as e:
            logger.error(f"Error while checking the activation token: {e}")

            raise ActivationTokenError("Wrong token")

        if not token_verified:
            raise ActivationTokenError("Wrong token")

        group = Group.objects.get(name=self.DEFAULT_ACTIVE_USER_GROUP)
        user.groups.set([group])


@cache
def get_user_service():
    return UserService(
        token_service=activation_token_service,
        email_service=get_user_email_service()
    )
