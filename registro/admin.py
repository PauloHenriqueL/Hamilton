from django.contrib import admin
from . import models

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('vlr_pago', 'qnt_consultas', 'is_pago')
    search_fields = ('vlr_pago', 'qnt_consultas')

admin.site.register(models.Registro, RegistroAdmin)