from django.contrib import admin
from . import models


class ClinicaAdmin(admin.ModelAdmin):
    list_display = ('clinica',)
    search_fields = ('clinica',)

admin.site.register(models.Clinica, ClinicaAdmin)