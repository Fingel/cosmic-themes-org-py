from django.contrib import admin
from themes.models import Theme

admin.site.register(Theme, admin.ModelAdmin)

# Register your models here.
