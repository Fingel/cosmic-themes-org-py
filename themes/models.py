from django.db import models
from django.urls import reverse
import logging
import re

logger = logging.getLogger(__name__)


class Theme(models.Model):
    name = models.CharField(max_length=200)
    ron = models.TextField()
    css = models.TextField(blank=True, default="")
    author = models.CharField(blank=True, default="", max_length=200)
    link = models.URLField(blank=True, default="")
    downloads = models.PositiveIntegerField(blank=True, default=0, editable=False)
    approved = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def is_dark(self) -> bool:
        regex = r"--is-dark: (\d);"
        if match := re.search(regex, self.css):
            return bool(int(match.group(1)))
        return False

    @property
    def popularity(self):
        return self.downloads

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("theme:list")
