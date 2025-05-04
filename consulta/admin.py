from django.contrib import admin
from . import models

class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('pk_consulta', 'dat_consulta')
    search_fields = ('pk_consulta', 'dat_consulta')

admin.site.register(models.Consulta, AtendimentoAdmin)