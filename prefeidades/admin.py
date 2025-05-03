from django.contrib import admin
from . import models


class PrefeIdadeAdmin(admin.ModelAdmin):
    list_display = ('prefeidade',)
    search_fields = ('prefeidade',)

admin.site.register(models.Prefeidade, PrefeIdadeAdmin)