from django.db import models
from terapeuta.models import Terapeuta
from paciente.models import Paciente
from django.core.validators import MinValueValidator, MaxValueValidator


class Desistencia_alta(models.Model):
    pk_desistencia_alta = models.AutoField(primary_key=True, verbose_name="ID")
    fk_terapeuta = models.ForeignKey(
        Terapeuta, 
        on_delete=models.CASCADE, 
        db_column='fk_terapeuta',
        verbose_name="Terapeuta"
    )
   
    fk_paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        db_column='fk_paciente',
        verbose_name="Paciente"
    )

    momento = models.CharField(
        verbose_name="Momento da saida?",
        choices=[('Antes da primeira sessao', 'Antes da primeira sessao'), ('No primeiro atendimento', 'No primeiro atendimento'), ('Depois do primeiro atendimento', 'depois do primeiro atendimento')],
    )

    motivo = models.CharField(
        null=True,
        blank=True,
        verbose_name="Motivo da saida?",
        choices=[('Alta', 'Alta'), ('Desistência', 'Desistência')],
    )


    relatorio = models.TextField(
        null=True,
        blank=True,
        verbose_name="Relatório de saída",
        help_text='Hipoteses clinicas para ocorrência' 
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        db_table = '"hamilton"."desistencia_alta"'
        verbose_name = "Desistencia/Alta"
        verbose_name_plural = "Desistencia/Alta"


