from django.contrib import admin
from . import models

class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('dat_consulta',)
    search_fields = ('dat_consulta',)

admin.site.register(models.Firstkiss, AtendimentoAdmin)