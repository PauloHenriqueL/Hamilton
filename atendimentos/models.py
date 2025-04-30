from django.db import models
from django.utils import timezone
from decano.models import Decano
from terapeuta.models import Terapeuta
from paciente.models import Paciente



class Atendimento(models.Model):
    pk_atendimento = models.AutoField(primary_key=True)
    fk_decano = models.ForeignKey(Decano, on_delete=models.DO_NOTHING, db_column='fk_decano')
    fk_terapeuta = models.ForeignKey(Terapeuta, on_delete=models.DO_NOTHING, db_column='fk_terapeuta')
    fk_paciente = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING, db_column='fk_paciente')
    realizado = models.BooleanField(default=False, null=False)
    dat_atendimento = models.DateField(null=False)
    vlr_sessao = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    vlr_pago = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Atendimento {self.pk_atendimento} - Paciente: {self.fk_paciente.nome}"

    class Meta:
        managed = False
        db_table = '"hamilton"."atendimentos"'
