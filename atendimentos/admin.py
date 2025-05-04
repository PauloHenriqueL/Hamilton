from django.contrib import admin
from . import models

class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('pk_atendimento', 'fk_decano', 'fk_terapeuta')
    search_fields = ('fk_terapeuta__nome', 'fk_paciente__nome')

admin.site.register(models.Atendimentos, AtendimentoAdmin)