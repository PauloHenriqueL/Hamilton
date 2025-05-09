from django.db import models
from decano.models import Decano
from terapeuta.models import Terapeuta
from paciente.models import Paciente


class Firstkiss(models.Model):
    pk_firstkiss = models.AutoField(primary_key=True, verbose_name="ID")
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
    dat_consulta = models.DateField(verbose_name="Data da primeira sessão")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        db_table = '"hamilton"."firstkiss"'
        verbose_name = "Firstkiss"
        verbose_name_plural = "Firstkiss"

