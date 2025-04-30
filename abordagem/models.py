from django.db import models
from django.utils import timezone


class Abordagem(models.Model):
    pk_abordagem = models.AutoField(primary_key=True)
    abordagem = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.abordagem

    class Meta:
        managed = False
        db_table = '"hamilton"."abordagens"'
