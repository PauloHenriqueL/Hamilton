from django.db import models
from django.utils import timezone


class Nucleo(models.Model):
    pk_nucleo = models.AutoField(primary_key=True, verbose_name="ID")
    nucleo = models.CharField(max_length=30, verbose_name="Núcleo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nucleo

    class Meta:
        managed = False
        db_table = '"hamilton"."nucleos"'
        verbose_name = "Núcleo"
        verbose_name_plural = "Núcleos"