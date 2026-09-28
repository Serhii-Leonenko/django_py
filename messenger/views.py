from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

# from messenger.forms import MessageForm
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


# --------------------------List View =================================
class MessageListView(ListView):
    model = Message


# --------------------------Detail View ================================
class MessageDetailView(DetailView):
    model = Message

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj:
            self.request.session["last_viewed_message"] = obj.id

        return obj


# -------------------------Create View----------------------------------
# class MessageCreateView(View):
#     def get(self, request):
#         form = MessageForm()
#
#         return render(
#             request=request,
#             template_name="messenger/message_form.html",
#             context={"form": form}
#         )
#
#     def post(self, request):
#         form = MessageForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#
#             return redirect(reverse("messenger:message-list"))
#
#         return render(
#             request=request,
#             template_name="messenger/message_form.html",
#             context={"form": form}
#         )


class MessageCreateView(CreateView):
    model = Message
    fields = ["text"]
    success_url = reverse_lazy("messenger:message-list")
