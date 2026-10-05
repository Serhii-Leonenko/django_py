from functools import cache

from django.core.mail import  EmailMessage
from django.template.loader import render_to_string


class UserEmailService:
    ACTIVATION_SUBJECT = "Activate your Messenger account"
    ACTIVATION_HTML_TEMPLATE = "emails/user_activation.html"

    def send_activation_email(self, username: str, email: str, activation_link: str):
        context = {"username": username, "activation_link": activation_link}

        message = EmailMessage(
            subject=self.ACTIVATION_SUBJECT,
            body=render_to_string(self.ACTIVATION_HTML_TEMPLATE, context),
            to=[email],
        )
        message.content_subtype = "html"
        message.send()


@cache
def get_user_email_service():
    return UserEmailService()
