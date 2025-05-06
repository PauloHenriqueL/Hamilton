from django.db import models
from django.utils import timezone
from captacao.models import Captacao


class Paciente(models.Model):
    pk_paciente = models.AutoField(primary_key=True, verbose_name="ID")
    fk_captacao = models.ForeignKey(
        Captacao, 
        on_delete=models.CASCADE, 
        db_column='fk_captacao',
        verbose_name="Captação"
    )
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    contato_apoio = models.CharField(max_length=20, verbose_name="Contato de Apoio")
    dat_nascimento = models.DateField(verbose_name="Data de Nascimento")
    vlr_sessao = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Sessão")
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
        managed = False
        ordering = ['nome']
        db_table = '"hamilton"."pacientes"'
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"