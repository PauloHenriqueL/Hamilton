from django.db import models
from django.utils import timezone
from terapeuta.models import Terapeuta


class Prefeidade(models.Model):
    pk_prefeidade = models.AutoField(primary_key=True)
    fk_terapeuta = models.ForeignKey(Terapeuta, on_delete=models.DO_NOTHING, db_column='fk_terapeuta')
    infantil = models.BooleanField(deafult='false')
    adolescente = models.BooleanField(deafult='false')
    adulto = models.BooleanField(deafult='false')
    idoso = models.BooleanField(deafult='false')
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.prefeidade

    class Meta:
        managed = False
        db_table = '"hamilton"."prefeidades"'
