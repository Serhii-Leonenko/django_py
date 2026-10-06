from django import forms

from core.mixins import BootstrapFormMixin
from messenger.models import Message


class MessageForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a message..."}),
        }
        labels = {"text": ""}
