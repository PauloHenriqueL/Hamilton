from django.db import models
from django.utils import timezone



class Decano(models.Model):
    pk_decano = models.AutoField(primary_key=True, verbose_name="ID")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    dat_nascimento = models.DateField(verbose_name="Data de Nascimento")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        ordering = ['nome']
        db_table = '"hamilton"."decanos"'
        verbose_name = "Decano"
        verbose_name_plural = "Decanos"
   
    def __str__(self):
        return self.nome
