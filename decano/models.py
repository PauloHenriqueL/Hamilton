from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
import datetime


class Decano(models.Model):
    pk_decano = models.AutoField(primary_key=True)
    nome = models.TextField(null=False)
    usuario = models.TextField(null=False, unique=True)
    email = models.TextField(null=False, unique=True)
    telefone = models.CharField(max_length=20, null=False)
    dat_nascimento = models.DateField(null=False)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        ordering = ['nome']
        verbose_name = 'Decano'
        db_table = '"hamilton"."decanos"'

    def __str__(self):
        return self.nome
