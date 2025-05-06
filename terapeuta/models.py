from django.db import models
from django.utils import timezone
import datetime
from decano.models import Decano
from abordagem.models import Abordagem
from nucleo.models import Nucleo
from clinicas.models import Clinica
from modalidades.models import Modalidade


class Terapeuta(models.Model):
    pk_terapeuta = models.AutoField(primary_key=True, verbose_name="ID")
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
    fk_nucleo = models.ForeignKey(
        Nucleo, 
        on_delete=models.CASCADE, 
        db_column='fk_nucleo',
        verbose_name="Núcleo"
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
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    dat_nascimento = models.DateField(verbose_name="Data de Nascimento")
    sexo = models.CharField(
        max_length=1, 
        choices=[('M', 'Masculino'), ('F', 'Feminino')],
        verbose_name="Sexo"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        ordering = ['nome']
        db_table = '"hamilton"."terapeutas"'
        verbose_name = "Terapeuta"
        verbose_name_plural = "Terapeutas"
    
    def __str__(self):
        return self.nome