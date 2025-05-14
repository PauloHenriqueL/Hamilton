from django.contrib import admin
from . import models

class Desistencia_altaAdmin(admin.ModelAdmin):
    list_display = ('motivo',)
    search_fields = ('motivo',)



admin.site.register(models.Desistencia_alta, Desistencia_altaAdmin)