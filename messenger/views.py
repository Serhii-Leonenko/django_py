from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from messenger.forms import MessageForm
from messenger.models import Message


# --------------------------Home view-----------------------------
class HomeView(TemplateView):
    template_name = "messenger/home.html"

    def _get_last_viewed_message(self) -> Message | None:
        if last_viewed_message_id := self.request.session.get("last_viewed_message"):
            try:
                return Message.objects.get(id=last_viewed_message_id)
            except Message.DoesNotExist:
                self.request.session.pop("last_viewed_message")

                return None

        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_messages"] = Message.objects.count()

        if last_viewed_message := self._get_last_viewed_message():
            context["last_viewed_message"] = last_viewed_message

        return context


class MessageListView(PermissionRequiredMixin, ListView):
    model = Message
    permission_required = "messenger.view_message"

    def get_queryset(self):
        queryset = super().get_queryset()

        if query := self.request.GET.get("q"):
            queryset = queryset.filter(text__icontains=query)

        return queryset

    def get_context_data(
        self,
        *,
        object_list = None,
        **kwargs
    ):
        context = super().get_context_data(object_list=object_list, **kwargs)

        if self.request.user.has_perm("messenger.add_message"):
            form = MessageForm()
            context["form"] = form

        return context


class MessageDetailView(PermissionRequiredMixin, DetailView):
    model = Message
    permission_required = "messenger.view_message"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj:
            self.request.session["last_viewed_message"] = obj.id

        return obj


class MessageCreateView(PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("messenger:message-list")
    permission_required = "messenger.add_message"
