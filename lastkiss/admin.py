from django.contrib import admin
from . import models

class LastkissAdmin(admin.ModelAdmin):
    list_display = ('consentimento_paciente','bem_estar')
    search_fields = ('consentimento_paciente','bem_estar')

admin.site.register(models.Lastkiss, LastkissAdmin)