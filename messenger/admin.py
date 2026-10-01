from django.contrib import admin

from messenger.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
