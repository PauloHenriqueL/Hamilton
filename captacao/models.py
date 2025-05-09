from django.db import models
from django.utils import timezone


class Captacao(models.Model):
    pk_captacao = models.AutoField(primary_key=True, verbose_name="ID")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = '"hamilton"."captacoes"'
        verbose_name = "Captação"
        verbose_name_plural = "Captações"
