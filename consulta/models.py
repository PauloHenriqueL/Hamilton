from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decano.models import Decano
from terapeuta.models import Terapeuta
from paciente.models import Paciente


class Consulta(models.Model):
    CANCELAMENTO_CHOICES = [
        ('T', 'Terapeuta'),
        ('P', 'Paciente'),
    ]
    pk_consulta = models.AutoField(primary_key=True)
    fk_decano = models.ForeignKey(Decano, on_delete=models.DO_NOTHING, db_column='fk_decano')
    fk_terapeuta = models.ForeignKey(
        Terapeuta,
        on_delete=models.CASCADE,
        db_column='fk_terapeuta'
    )
    fk_paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        db_column='fk_paciente'
    )
    dat_consulta = models.DateField(null=True, blank=True)
    vlr_consulta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_realizado = models.BooleanField()
    is_pago = models.BooleanField(null=True, blank=True)
    vlr_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    quem_cancelou = models.CharField(
        max_length=1,
        choices=CANCELAMENTO_CHOICES,
        null=True,
        blank=True
    )
    motivo_cancelamento = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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