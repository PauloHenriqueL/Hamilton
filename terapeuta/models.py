from django.db import models
from decano.models import Decano
from abordagem.models import Abordagem
from associado.models import Associado
from clinicas.models import Clinica
from modalidades.models import Modalidade


class Terapeuta(models.Model):
    pk_terapeuta = models.AutoField(primary_key=True, verbose_name="ID")
    fk_associado = models.ForeignKey(
        Associado, 
        on_delete=models.CASCADE, 
        db_column='fk_associado',
        verbose_name="Associado"
    )
    fk_decano = models.ForeignKey(
        Decano, 
        on_delete=models.CASCADE, 
        db_column='fk_decano',
        verbose_name="Decano"
    )
    fk_abordagem = models.ForeignKey(
        Abordagem, 
        on_delete=models.CASCADE, 
        db_column='fk_abordagem',
        verbose_name="Abordagem"
    )
    fk_clinica = models.ForeignKey(
        Clinica, 
        on_delete=models.CASCADE, 
        db_column='fk_clinica',
        verbose_name="Clínica"
    )
    fk_modalidade = models.ForeignKey(
        Modalidade, 
        on_delete=models.CASCADE, 
        db_column='fk_modalidade',
        verbose_name="Modalidade"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        ordering = ['-updated_at']
        db_table = '"hamilton"."terapeutas"'
        verbose_name = "Terapeuta"
        verbose_name_plural = "Terapeutas"
    
    def __str__(self):
        return f"Terapeuta {self.fk_associado}"