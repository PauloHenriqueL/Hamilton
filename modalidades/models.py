from django.db import models
from django.utils import timezone


class Modalidade(models.Model):
    pk_modalidade = models.AutoField(primary_key=True, verbose_name="ID")
    modalidade = models.CharField(max_length=10, verbose_name="Modalidade")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.modalidade
    
    class Meta:
        db_table = '"hamilton"."modalidades"'
        verbose_name = "Modalidade"
        verbose_name_plural = "Modalidades"
