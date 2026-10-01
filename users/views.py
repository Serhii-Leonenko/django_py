from django.shortcuts import render

from users.services import UserService


class UserRegisterView(...):
    user_service = UserService()

    def get(self, request):
        ...

    def post(self, request):
        form = Form(request.POST)

        if form.is_valid():
            self.user_service.create_user(**form.cleaned_data)