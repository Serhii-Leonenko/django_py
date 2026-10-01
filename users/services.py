from django.db import transaction

from users.models import Profile


class UserService:
    def create_user(self, username, email, password):
        with transaction.atomic():
            user = User.objects.create_user(username, email, password)
            Profile.objects.create(user=user)

        return user
