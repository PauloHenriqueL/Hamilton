from django.contrib import admin
from . import models


class DecanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'dat_nascimento', 'is_active')
    search_fields = ('nome', 'email')
    list_filter = ('is_active',)

admin.site.register(models.Decano, DecanoAdmin)