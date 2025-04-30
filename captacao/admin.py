from django.contrib import admin
from . import models


class CaptacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'is_active')
    search_fields = ('nome',)
    list_filter = ('is_active',)

admin.site.register(models.Captacao, CaptacaoAdmin)
