from django.contrib import admin
from . import models


class AbordagemAdmin(admin.ModelAdmin):
    list_display = ('abordagem',)
    search_fields = ('abordagem',)


admin.site.register(models.Abordagem, AbordagemAdmin)