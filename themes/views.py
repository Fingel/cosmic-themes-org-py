from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from themes.models import Theme

from .filters import color_distance, themes_name, themes_order
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
    success_message = (
        "Thanks for submitting a theme! If you would like to edit or remove your "
        'submission, please open an issue on <a href="https://github.com/Fingel/cosmic-themes-org-py/">'
        "Github</a>."
    )

    def get_success_url(self) -> str:
        if self.object:
            notify_theme_created(self.object)
        return super().get_success_url()


class ThemeListView(ListView):
    model = Theme
    ordering = ["-downloads"]
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().filter(approved=True)

        if query := self.request.GET.get("search", ""):
            qs = themes_name(qs, query)

        if sort := self.request.GET.get("sort", ""):
            qs = themes_order(qs, sort)

        if color := self.request.GET.get("color", ""):
            r, g, b = color.split(",")
            qs = color_distance(qs, (int(r), int(g), int(b)))

        return qs

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return ["themes/theme_list_partial.html"]
        else:
            return super().get_template_names()


class ThemeDetailView(DetailView):
    model = Theme

    def get_queryset(self):
        return super().get_queryset().filter(approved=True)


class ThemeDownloadView(View):
    def post(self, request, id):
        theme = get_object_or_404(Theme, pk=id, approved=True)
        Theme.objects.filter(pk=id).update(downloads=F("downloads") + 1)
        response = HttpResponse(theme.ron, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={theme.name}.ron"
        return response
