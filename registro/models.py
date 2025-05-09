from django.db import models
from decano.models import Decano
from terapeuta.models import Terapeuta
from paciente.models import Paciente


class Registro(models.Model):
    pk_registro = models.AutoField(primary_key=True, verbose_name="ID")
    fk_decano = models.ForeignKey(
        Decano, 
        on_delete=models.CASCADE, 
        db_column='fk_decano',
        verbose_name="Decano"
    )
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
    qnt_consultas = models.IntegerField(verbose_name="Quantidade de consultas realizados no mês")
    vlr_consulta = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Valor da Consulta",
        help_text="Informe o total de cada consulta"
    )
    is_pago = models.BooleanField(verbose_name="Pago")
    vlr_pago = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor Pago",
        help_text="Informe o total recebido no pix"
    )
    qnt_consultas_nao = models.IntegerField(verbose_name="Quantidade de consultas não realizadas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        db_table = '"hamilton"."registro"'
        managed=False
        verbose_name = "Registro"
        verbose_name_plural = "Registro Mensal"        
