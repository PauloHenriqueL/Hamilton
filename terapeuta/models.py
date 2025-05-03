from django.db import models
from django.utils import timezone
import datetime
from decano.models import Decano
from abordagem.models import Abordagem
from nucleo.models import Nucleo
from clinicas.models import Clinica
from modalidades.models import Modalidade



class Terapeuta(models.Model):
    pk_terapeuta = models.AutoField(primary_key=True)
    nome = models.TextField(null=False)
    usuario = models.TextField(null=False, unique=True)
    email = models.TextField(null=False, unique=True)
    telefone = models.CharField(max_length=20, null=False)
    dat_nascimento = models.DateField(null=False)
    sexo = models.CharField(max_length=1, null=False)
    fk_decano = models.ForeignKey(Decano, on_delete=models.DO_NOTHING, db_column='fk_decano')
    fk_abordagem = models.ForeignKey(Abordagem, on_delete=models.DO_NOTHING, db_column='fk_abordagem')
    fk_nucleo = models.ForeignKey(Nucleo, on_delete=models.DO_NOTHING, db_column='fk_nucleo')
    fk_clinica = models.ForeignKey(Clinica, on_delete=models.DO_NOTHING, db_column='fk_clinica')
    fk_modalidade = models.ForeignKey(Modalidade, on_delete=models.DO_NOTHING, db_column='fk_modalidade')
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        ordering = ['nome']
        db_table = '"hamilton"."terapeutas"'
# teste
    def __str__(self):
        return self.nome