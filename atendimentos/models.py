from django.db import models
from django.utils import timezone
from decano.models import Decano
from terapeuta.models import Terapeuta
from paciente.models import Paciente
from django.core.validators import MinValueValidator, MaxValueValidator


class Atendimentos(models.Model):
    pk_atendimento = models.AutoField(primary_key=True)
    fk_decano = models.ForeignKey(
        Decano, 
        on_delete=models.CASCADE,
        db_column='fk_decano'
    )
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
    ano = models.IntegerField()
    mes = models.IntegerField(validators=[MaxValueValidator(12)])
    qtd_consulta = models.IntegerField(validators=[MinValueValidator(0)])
    vlr_consulta = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Atendimento {self.pk_atendimento} - Paciente: {self.fk_paciente.nome}"

    class Meta:
        managed = False
        db_table = '"hamilton"."atendimentos"'