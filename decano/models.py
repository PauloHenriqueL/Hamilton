from django.db import models
from associado.models import Associado



class Decano(models.Model):
    pk_decano = models.AutoField(primary_key=True, verbose_name="ID")
    fk_associado = models.ForeignKey(
        Associado, 
        on_delete=models.CASCADE, 
        db_column='fk_associado',
        verbose_name="Associado"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        ordering = ['-updated_at']
        db_table = '"hamilton"."decanos"'
        verbose_name = "Decano"
        verbose_name_plural = "Decanos"
   
    def __str__(self):
        return f"Decano {self.fk_associado}"
