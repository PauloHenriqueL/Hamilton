from django.contrib import admin
from . import models


class PrefeIdadeAdmin(admin.ModelAdmin):
    list_display = ('pk_prefeidade',)
    search_fields = ('pk_prefeidade',)

admin.site.register(models.Prefeidade, PrefeIdadeAdmin)