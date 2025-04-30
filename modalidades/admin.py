from django.contrib import admin
from . import models


class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('modalidade',)
    search_fields = ('modalidade',)

admin.site.register(models.Modalidade, ModalidadeAdmin)