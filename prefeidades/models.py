from django.db import models
from django.utils import timezone


class Prefeidade(models.Model):
    pk_prefeidade = models.AutoField(primary_key=True)
    prefeidade = models.CharField(max_length=20, null=False)
    idade_maxima = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
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
