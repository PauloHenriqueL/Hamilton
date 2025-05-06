from django.db import models
from django.utils import timezone
from terapeuta.models import Terapeuta


class Prefeidade(models.Model):
    pk_prefeidade = models.AutoField(primary_key=True, verbose_name="ID")
    fk_terapeuta = models.OneToOneField(
        Terapeuta, 
        on_delete=models.CASCADE, 
        db_column='fk_terapeuta',
        verbose_name="Terapeuta"
    )
    is_infantil = models.BooleanField(default=False, verbose_name="Atende Infantil")
    is_adolescente = models.BooleanField(default=False, verbose_name="Atende Adolescente")
    is_adulto = models.BooleanField(default=False, verbose_name="Atende Adulto")
    is_idoso = models.BooleanField(default=False, verbose_name="Atende Idoso")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")


    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


    class Meta:
        managed = False
        db_table = '"hamilton"."prefeidades"'
        constraints = [
            models.UniqueConstraint(
                fields=['fk_terapeuta'], 
                name='unique_terapeuta_prefeidade'
            )
        ]
        verbose_name = "Preferência de Idade"
        verbose_name_plural = "Preferências de Idade"