from django.db import models
from django.utils import timezone


class Clinica(models.Model):
    pk_clinica = models.AutoField(primary_key=True, verbose_name="ID")
    clinica = models.CharField(max_length=10, verbose_name="Clínica")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.clinica

    class Meta:
        managed=False
        db_table = '"hamilton"."clinicas"'
        verbose_name = "Clínica"
        verbose_name_plural = "Clínicas"