from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Captacao(models.Model):
    pk_captacao = models.AutoField(primary_key=True, verbose_name="ID")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = '"hamilton"."captacoes"'
        verbose_name = "Captação"
        verbose_name_plural = "Captações"

class Clinica(models.Model):
    pk_clinica = models.AutoField(primary_key=True, verbose_name="ID")
    clinica = models.CharField(max_length=10, verbose_name="Clínica")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.clinica

    class Meta:
        db_table = '"hamilton"."clinicas"'
        verbose_name = "Clínica"
        verbose_name_plural = "Clínicas"

class Modalidade(models.Model):
    pk_modalidade = models.AutoField(primary_key=True, verbose_name="ID")
    modalidade = models.CharField(max_length=10, verbose_name="Modalidade")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.modalidade
    
    class Meta:
        db_table = '"hamilton"."modalidades"'
        verbose_name = "Modalidade"
        verbose_name_plural = "Modalidades"

class Nucleo(models.Model):
    pk_nucleo = models.AutoField(primary_key=True, verbose_name="ID")
    nucleo = models.CharField(max_length=30, verbose_name="Núcleo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nucleo

    class Meta:
        db_table = '"hamilton"."nucleos"'
        verbose_name = "Núcleo"
        verbose_name_plural = "Núcleos"

class Abordagem(models.Model):
    pk_abordagem = models.AutoField(primary_key=True, verbose_name="ID")
    abordagem = models.CharField(max_length=255, verbose_name="Abordagem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.abordagem

    class Meta:
        db_table = '"hamilton"."abordagens"'
        verbose_name = "Abordagem"
        verbose_name_plural = "Abordagens"

class Prefeidade(models.Model):
    pk_prefeidade = models.AutoField(primary_key=True, verbose_name="ID")
    fk_terapeuta = models.OneToOneField(
        'principais.Terapeuta',  # Usando referência por string
        on_delete=models.CASCADE, 
        db_column='fk_terapeuta',
        verbose_name="Terapeuta"
    )
    is_infantil = models.BooleanField(default=False, verbose_name="Atende Infantil")
    is_adolescente = models.BooleanField(default=False, verbose_name="Atende Adolescente")
    is_adulto = models.BooleanField(default=False, verbose_name="Atende Adulto")
    is_idoso = models.BooleanField(default=False, verbose_name="Atende Idoso")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = '"hamilton"."prefeidades"'
        constraints = [
            models.UniqueConstraint(
                fields=['fk_terapeuta'], 
                name='unique_terapeuta_prefeidade'
            )
        ]
        verbose_name = "Preferência de Idade"
        verbose_name_plural = "Preferências de Idade"


class TerapeutaUser(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Usuário"
    )
    terapeuta = models.OneToOneField(
        'principais.Terapeuta',
        on_delete=models.CASCADE, 
        db_column='fk_terapeuta',
        verbose_name="Terapeuta"
    )
    
    class Meta:
        managed = False  # Manter se você não quer que o Django gerencie essa tabela
        db_table = '"hamilton"."terapeuta_usuarios"'
        constraints = [
            models.UniqueConstraint(
                fields=['terapeuta'], 
                name='unique_terapeuta_user'
            )
        ]
        verbose_name = "Usuário de Terapeuta"
        verbose_name_plural = "Usuários de Terapeutas"
        
    def __str__(self):
        return f"{self.usuario.username} - {self.terapeuta.nome if self.terapeuta else 'Sem terapeuta'}"