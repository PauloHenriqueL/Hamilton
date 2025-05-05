from django.contrib import admin
from . import models


class TerapeutaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'sexo', 'fk_decano', 'fk_abordagem', 'fk_nucleo', 'fk_clinica', 'fk_modalidade', 'is_active')
    search_fields = ('nome', 'email')
    list_filter = ('sexo', 'is_active', 'fk_abordagem', 'fk_nucleo', 'fk_clinica', 'fk_modalidade')

admin.site.register(models.Terapeuta, TerapeutaAdmin)