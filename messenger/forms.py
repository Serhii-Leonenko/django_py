from django import forms

from messenger.models import Message


# class MessageForm(forms.Form):
#     text = forms.CharField(
#         widget=forms.Textarea(),
#         min_length=5
#     )


# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ["text"]
