from django.contrib import admin
from . import models


class DecanoAdmin(admin.ModelAdmin):
    list_display = ('is_active',)
    search_fields = ('is_active',)
    list_filter = ('is_active',)

admin.site.register(models.Decano, DecanoAdmin)