from django.db import models
from django.utils import timezone
from captacao.models import Captacao


class Paciente(models.Model):
    pk_paciente = models.AutoField(primary_key=True)
    nome = models.TextField(null=False)
    email = models.TextField(null=False, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=False)
    contato_apoio = models.CharField(max_length=20, null=False)
    dat_nascimento = models.DateField(null=False)
    vlr_sessao = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    qtd_sessao = models.IntegerField(null=False)
    fk_captacao = models.ForeignKey(Captacao, on_delete=models.DO_NOTHING, db_column='fk_captacao')
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

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
