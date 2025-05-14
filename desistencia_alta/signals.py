from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Desistencia_alta
from paciente.models import Paciente

@receiver(post_save, sender=Desistencia_alta)
def desativar_paciente_ao_criar_desistencia_alta(sender, instance, created, **kwargs):
    """
    Signal que desativa um paciente (is_active = False) quando um registro
    de Desistencia_alta for criado para este paciente.
    """
    if created:  # Só executa na criação do registro, não em atualizações
        paciente = instance.fk_paciente
        if paciente.is_active:  # Verifica se o paciente está ativo
            paciente.is_active = False
            paciente.save(update_fields=['is_active'])  # Salva apenas o campo alterado