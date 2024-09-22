import logging
import re

from django.db import models
from django.urls import reverse

logger = logging.getLogger(__name__)


class Theme(models.Model):
    name = models.CharField(max_length=200)
    ron = models.TextField()
    css = models.TextField(blank=True, default="")
    author = models.CharField(blank=True, default="", max_length=200)
    link = models.URLField(blank=True, default="")
    downloads = models.PositiveIntegerField(blank=True, default=0, editable=False)
    approved = models.BooleanField(default=True)
    red = models.IntegerField(default=0)
    green = models.IntegerField(default=0)
    blue = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def is_dark(self) -> bool:
        regex = r"--is-dark: (\d);"
        if match := re.search(regex, self.css):
            return bool(int(match.group(1)))
        return False

    @property
    def accent_color(self) -> tuple[int, int, int]:
        regex = r"--accent-color: rgba\((\d+), (\d+), (\d+)"
        if match := re.search(regex, self.css):
            return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return (0, 0, 0)

    @property
    def popularity(self):
        return self.downloads

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("theme:list")
