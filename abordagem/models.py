from django.db import models
from django.utils import timezone


class Abordagem(models.Model):
    pk_abordagem = models.AutoField(primary_key=True, verbose_name="ID")
    abordagem = models.CharField(max_length=255, verbose_name="Abordagem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.abordagem

    class Meta:
        managed = False
        db_table = '"hamilton"."abordagens"'
        verbose_name = "Abordagem"
        verbose_name_plural = "Abordagens"