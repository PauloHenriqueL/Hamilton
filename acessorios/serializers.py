from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from principais.models import Terapeuta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class TerapeutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terapeuta
        fields = ('pk_terapeuta', 'nome', 'email')
        read_only_fields = ('pk_terapeuta',)

class TerapeutaUserSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    terapeuta = TerapeutaSerializer(read_only=True)
    terapeuta_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = models.TerapeutaUser
        fields = ('id', 'usuario', 'terapeuta', 'terapeuta_id')
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        terapeuta_id = validated_data.pop('terapeuta_id')
        
        # Cria o usuário
        password = usuario_data.pop('password', None)
        user = User.objects.create(**usuario_data)
        if password:
            user.set_password(password)
            user.save()
        
        # Busca o terapeuta
        terapeuta = Terapeuta.objects.get(pk_terapeuta=terapeuta_id)
        
        # Cria o TerapeutaUser
        return models.TerapeutaUser.objects.create(usuario=user, terapeuta=terapeuta)





class AbordagemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Abordagem
        fields = '__all__'

class NucleoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Nucleo
        fields = '__all__'

class CaptacaoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Captacao
        fields = '__all__'

class ClinicaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Clinica
        fields = '__all__'

class ModalidadeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Modalidade
        fields = '__all__'

class PrefeidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Prefeidade
        fields = '__all__'