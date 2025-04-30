from django.contrib import admin
from . import models


class NucleoAdmin(admin.ModelAdmin):
    list_display = ('nucleo',)
    search_fields = ('nucleo',)

admin.site.register(models.Nucleo, NucleoAdmin)