from django.db import models
from django.utils import timezone
from terapeuta.models import Terapeuta


class Prefeidade(models.Model):
    pk_prefeidade = models.AutoField(primary_key=True)
    fk_terapeuta = models.ForeignKey(
        Terapeuta, 
        on_delete=models.DO_NOTHING, 
        db_column='fk_terapeuta'
    )
    is_infantil = models.BooleanField(default=False, null=False)
    is_adolescente = models.BooleanField(default=False, null=False)
    is_adulto = models.BooleanField(default=False, null=False)
    is_idoso = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


    class Meta:
        managed = False
        db_table = '"hamilton"."prefeidades"'
        constraints = [
            models.UniqueConstraint(
                fields=['fk_terapeuta'], 
                name='unique_terapeuta_prefeidade'
            )
        ]
