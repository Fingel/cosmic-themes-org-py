from django.urls import path

from .views import ThemeCreateView, ThemeDetailView, ThemeDownloadView, ThemeListView

app_name = "themes"
urlpatterns = [
    path("", ThemeListView.as_view(), name="list"),
    path("create/", ThemeCreateView.as_view(), name="create"),
    path("<int:pk>/", ThemeDetailView.as_view(), name="detail"),
    path("<int:id>/download/", ThemeDownloadView.as_view(), name="download"),
]
