from rest_framework import generics
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import TerapeutaUser
from .forms import TerapeutaUserForm
from principais.models import Terapeuta, Consulta

# View para login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo, {username}!")
                return redirect('consulta-list')
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# View para logout
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('login')

# View para criar um usuário para um terapeuta existente
@login_required
def create_terapeuta_user(request, pk_terapeuta):
    # Verificar se o usuário tem permissão para criar usuários
    if not request.user.has_perm('auth.add_user'):
        messages.error(request, "Você não tem permissão para criar usuários.")
        return redirect('consulta-list')
        
    terapeuta = get_object_or_404(Terapeuta, pk_terapeuta=pk_terapeuta)
    
    # Verifica se o terapeuta já tem um usuário
    existing_user = TerapeutaUser.objects.filter(terapeuta=terapeuta).exists()
    if existing_user:
        messages.warning(request, "Este terapeuta já possui um usuário associado.")
        return redirect('consulta-list')
    
    if request.method == 'POST':
        form = TerapeutaUserForm(request.POST)
        if form.is_valid():
            user = form.save(terapeuta=terapeuta)
            messages.success(request, f"Usuário criado com sucesso para {terapeuta.nome}!")
            return redirect('consulta-list')
    else:
        form = TerapeutaUserForm(initial={'email': terapeuta.email})
    
    return render(request, 'acessorios/create_terapeuta_user.html', {
        'form': form,
        'terapeuta': terapeuta
    })



class AbordagemListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Abordagem.objects.all()
    serializer_class = serializers.AbordagemSerializer  # Corrigido aqui


class AbordagemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Abordagem.objects.all()
    serializer_class = serializers.AbordagemSerializer  # Corrigido aqui


class CaptacaoListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Captacao.objects.all()
    serializer_class = serializers.CaptacaoSerializer  # Corrigido aqui


class CaptacaoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Captacao.objects.all()
    serializer_class = serializers.CaptacaoSerializer  # Corrigido aqui


class ClinicaListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Clinica.objects.all()
    serializer_class = serializers.ClinicaSerializer  # Corrigido aqui


class ClinicaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Clinica.objects.all()
    serializer_class = serializers.ClinicaSerializer  # Corrigido aqui


class ModalidadeListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Modalidade.objects.all()
    serializer_class = serializers.ModalidadeSerializer  # Corrigido aqui


class ModalidadeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Modalidade.objects.all()
    serializer_class = serializers.ModalidadeSerializer  # Corrigido aqui


class NucleoListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Nucleo.objects.all()
    serializer_class = serializers.NucleoSerializer  # Corrigido aqui


class NucleoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Nucleo.objects.all()
    serializer_class = serializers.NucleoSerializer  # Corrigido aqui


class PrefeidadeListCreateAPIView(generics.ListCreateAPIView):  # Padronizado o nome da classe
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Prefeidade.objects.all()
    serializer_class = serializers.PrefeidadeSerializer  # Corrigido aqui


class PrefeidadeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # Corrigido o nome da classe e tipo de view
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = models.Prefeidade.objects.all()
    serializer_class = serializers.PrefeidadeSerializer  # Corrigido aqui