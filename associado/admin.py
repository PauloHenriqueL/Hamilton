from django.contrib import admin
from .models import Setor, Associado

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('setor', 'created_at')
    search_fields = ('setor',)

@admin.register(Associado)
class AssociadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    search_fields = ('nome',)
