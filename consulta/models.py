from django.db import models
from decano.models import Decano
from terapeuta.models import Terapeuta
from paciente.models import Paciente


class Consulta(models.Model):
    pk_consulta = models.AutoField(primary_key=True, verbose_name="ID")
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
    dat_consulta = models.DateField(verbose_name="Data da Consulta")
    vlr_consulta = models.IntegerField(verbose_name="Valor da Consulta")
    is_realizado = models.BooleanField(verbose_name="Realizada")
    is_pago = models.BooleanField(null=True, blank=True, verbose_name="Paga")
    vlr_pago = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Valor Pago"
    )
    quem_cancelou = models.CharField(
        max_length=1, 
        choices=[('T', 'Terapeuta'), ('P', 'Paciente')], 
        null=True, 
        blank=True,
        verbose_name="Quem Cancelou"
    )
    motivo_cancelamento = models.TextField(null=True, blank=True, verbose_name="Motivo do Cancelamento")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        db_table = '"hamilton"."consultas"'
        constraints = [
            models.CheckConstraint(
                check=models.Q(vlr_pago__gte=0),
                name='check_vlr_pago_greater_equal_0'
            ),
            models.CheckConstraint(
                check=models.Q(quem_cancelou__isnull=True) | models.Q(quem_cancelou__in=['T', 'P']),
                name='check_quem_cancelou_valid'
            ),
        ]