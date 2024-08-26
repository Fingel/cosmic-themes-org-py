from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import F
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.mail import send_mail

from themes.models import Theme
from .forms import ThemeForm


def notify_theme_created(theme: Theme):
    to_email = [settings.ADMINS[0][1]]
    subject = "A new theme has been submitted"
    message = "Moderate: https://cosmic-themes.org" + reverse_lazy(
        "admin:themes_theme_change", args=[theme.pk]
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to_email)


class ThemeCreateView(SuccessMessageMixin, CreateView):
    model = Theme
    form_class = ThemeForm
    success_message = "Thanks for submitting a theme! It looks great :)"

    def get_success_url(self) -> str:
        if self.object:
            notify_theme_created(self.object)
        return super().get_success_url()


class ThemeListView(ListView):
    queryset = Theme.objects.filter(approved=True)
    ordering = ["-downloads"]


class ThemeDownloadView(View):
    def post(self, request, id):
        theme = get_object_or_404(Theme, pk=id, approved=True)
        Theme.objects.filter(pk=id).update(downloads=F("downloads") + 1)
        response = HttpResponse(theme.ron, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={theme.name}.ron"
        return response
