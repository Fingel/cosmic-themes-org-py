from django.urls import path

from .views import ThemeCreateView, ThemeListView, ThemeDownloadView

app_name = "themes"
urlpatterns = [
    path("", ThemeListView.as_view(), name="list"),
    path("create/", ThemeCreateView.as_view(), name="create"),
    path("<int:id>/download/", ThemeDownloadView.as_view(), name="download"),
]
