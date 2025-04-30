from django.contrib import admin
from . import models


class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'email', 'telefone', 'contato_apoio', 'vlr_sessao', 'qtd_sessao', 'fk_captacao', 'is_active')
    search_fields = ('nome', 'usuario', 'email')
    list_filter = ('is_active', 'fk_captacao')

admin.site.register(models.Paciente, PacienteAdmin)