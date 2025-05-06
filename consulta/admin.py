from django.contrib import admin
from . import models

class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('vlr_consulta', 'dat_consulta')
    search_fields = ('vlr_consulta', 'dat_consulta')

admin.site.register(models.Consulta, AtendimentoAdmin)