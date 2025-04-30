from django.db import models
from django.utils import timezone


class Captacao(models.Model):
    pk_captacao = models.AutoField(primary_key=True)
    nome = models.TextField(null=False)
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
        db_table = '"hamilton"."captacoes"'
