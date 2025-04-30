from django.contrib import admin
from . import models

class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('pk_atendimento', 'fk_decano', 'fk_terapeuta', 'fk_paciente', 'realizado', 'dat_atendimento', 'vlr_sessao', 'vlr_pago', 'is_active')
    search_fields = ('fk_terapeuta__nome', 'fk_paciente__nome')
    list_filter = ('realizado', 'is_active', 'dat_atendimento', 'fk_decano')
    date_hierarchy = 'dat_atendimento'

admin.site.register(models.Atendimento, AtendimentoAdmin)