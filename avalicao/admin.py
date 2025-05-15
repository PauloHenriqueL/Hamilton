# avaliacao/admin.py
from django.contrib import admin
from .models import Avaliador, Avaliado, Avaliacao, Avalioracao

@admin.register(Avaliador)
class AvaliadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    search_fields = ('nome',)

@admin.register(Avaliado)
class AvaliadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    search_fields = ('nome',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('fk_avaliador', 'fk_avaliado', 'dat_avaliacao')
    list_filter = ('dat_avaliacao',)

@admin.register(Avalioracao)
class AvalioracaoAdmin(admin.ModelAdmin):
    list_display = ('fk_avaliador', 'fk_avaliado', 'dat_avaliacao')
    list_filter = ('dat_avaliacao',)
