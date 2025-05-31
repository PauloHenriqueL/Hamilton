from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse
from .models import Paciente
from django.views.decorators.http import require_GET
from decimal import Decimal
from acessorios.models import TerapeutaUser
from django.contrib import messages


@require_GET
def paciente_valor_sessao(request, pk):
    """Endpoint para obter o valor da sessão de um paciente"""
    try:
        paciente = Paciente.objects.get(pk=pk)
        return JsonResponse({'vlr_sessao': int(paciente.vlr_sessao)})
    except Paciente.DoesNotExist:
        return JsonResponse({'error': 'Paciente não encontrado'}, status=404)


class ConsultaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Consulta
    template_name = 'consulta_list.html'
    context_object_name = 'consultas'
    paginate_by = 10
    permission_required = 'principais.view_consulta'

    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: Usar select_related para reduzir queries
        queryset = models.Consulta.objects.select_related(
            'fk_terapeuta',                    # Dados do terapeuta
            'fk_paciente',                     # Dados do paciente
            'fk_terapeuta__fk_abordagem',      # Abordagem do terapeuta
            'fk_terapeuta__fk_clinica'         # Clínica do terapeuta
        ).order_by('-dat_consulta')           # Ordenar por data mais recente
        
        # Filtrar apenas consultas do terapeuta logado
        try:
            terapeuta_user = TerapeutaUser.objects.get(usuario=self.request.user)
            terapeuta = terapeuta_user.terapeuta
            queryset = queryset.filter(fk_terapeuta=terapeuta)
        except TerapeutaUser.DoesNotExist:
            if not self.request.user.is_staff:
                queryset = queryset.none()
        
        # Filtragem por nome
        nome = self.request.GET.get('nome')
        if nome:
            queryset = queryset.filter(
                Q(fk_paciente__nome__icontains=nome) | 
                Q(fk_terapeuta__nome__icontains=nome)
            )
        
        return queryset


class ConsultaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Consulta
    template_name = 'consulta_create.html'
    form_class = forms.ConsultaForm
    success_url = reverse_lazy('consulta-list')
    permission_required = 'principais.add_consulta'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        try:
            terapeuta_user = TerapeutaUser.objects.get(usuario=self.request.user)
            terapeuta = terapeuta_user.terapeuta
            
            form.fields['fk_terapeuta'].initial = terapeuta.pk_terapeuta
            form.fields['fk_terapeuta'].widget.attrs.update({
                'readonly': 'readonly',
                'style': 'pointer-events: none; background-color: #343a40 !important; color: #ffffff !important; border-color: #495057 !important;'
            })
            form.fields['fk_terapeuta'].queryset = form.fields['fk_terapeuta'].queryset.filter(pk=terapeuta.pk_terapeuta)
            
        except TerapeutaUser.DoesNotExist:
            pass
        
        return form
    
    def form_valid(self, form):
        quantidade = int(self.request.POST.get('quantidade', 1))
        vlr_pix_total_str = self.request.POST.get('vlr_pix_total', '')
        vlr_pix_total = float(vlr_pix_total_str) if vlr_pix_total_str and vlr_pix_total_str.strip() else None
        vlr_pago_por_consulta = None
        
        if vlr_pix_total:
            vlr_pago_por_consulta = round(vlr_pix_total / quantidade, 2)
        
        consulta = form.save(commit=False)
        
        try:
            terapeuta_user = TerapeutaUser.objects.get(usuario=self.request.user)
            consulta.fk_terapeuta = terapeuta_user.terapeuta
        except TerapeutaUser.DoesNotExist:
            if not consulta.fk_terapeuta:
                messages.error(self.request, 'Erro: Terapeuta não foi definido corretamente.')
                return self.form_invalid(form)
        
        consulta.is_realizado = self.request.POST.get('is_realizado_0', '') == 'on'
        
        if not consulta.is_realizado:
            consulta.is_pago = False
            consulta.vlr_pago = None
        else:
            consulta.is_pago = vlr_pago_por_consulta is not None
            consulta.vlr_pago = vlr_pago_por_consulta
        
        if 'data_consulta_0' in self.request.POST and self.request.POST['data_consulta_0']:
            consulta.dat_consulta = self.request.POST['data_consulta_0']
        
        consulta.save()
        
        if quantidade > 1:
            for i in range(1, quantidade):
                nova_consulta = models.Consulta(
                    fk_terapeuta=consulta.fk_terapeuta,
                    fk_paciente=consulta.fk_paciente,
                    vlr_consulta=consulta.vlr_consulta,
                )
                
                is_realizado_key = f'is_realizado_{i}'
                nova_consulta.is_realizado = self.request.POST.get(is_realizado_key, '') == 'on'
                
                if not nova_consulta.is_realizado:
                    nova_consulta.is_pago = False
                    nova_consulta.vlr_pago = None
                else:
                    nova_consulta.is_pago = vlr_pago_por_consulta is not None
                    nova_consulta.vlr_pago = vlr_pago_por_consulta
                
                data_key = f'data_consulta_{i}'
                if data_key in self.request.POST and self.request.POST[data_key]:
                    nova_consulta.dat_consulta = self.request.POST[data_key]
                
                nova_consulta.save()
        
        return redirect(self.success_url)


class ConsultaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Consulta
    template_name = 'consulta_detail.html'
    permission_required = 'principais.view_consulta'
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: Buscar dados relacionados junto
        return models.Consulta.objects.select_related(
            'fk_terapeuta',
            'fk_paciente',
            'fk_terapeuta__fk_abordagem',
            'fk_terapeuta__fk_clinica'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consulta = self.object
        
        if consulta.is_pago and consulta.vlr_pago is not None and consulta.vlr_consulta is not None:
            context['diferenca_valor'] = consulta.vlr_pago - consulta.vlr_consulta
        else:
            context['diferenca_valor'] = Decimal('0.00')
            
        return context


class ConsultaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Consulta
    template_name = 'consulta_update.html'
    form_class = forms.ConsultaForm
    success_url = reverse_lazy('consulta-list')
    permission_required = 'principais.change_consulta'
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: Buscar dados relacionados junto
        return models.Consulta.objects.select_related(
            'fk_terapeuta',
            'fk_paciente'
        )
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name in ['quantidade', 'vlr_pix_total']:
            if field_name in form.fields:
                del form.fields[field_name]
        return form


class ConsultaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Consulta
    template_name = 'consulta_delete.html'
    success_url = reverse_lazy('consulta-list')
    permission_required = 'principais.delete_consulta'
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: Buscar dados relacionados para mostrar no template
        return models.Consulta.objects.select_related(
            'fk_terapeuta',
            'fk_paciente'
        )


class AltaDesistenciaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Altadesistencia
    template_name = 'altadesistencia_create.html'
    form_class = forms.AltaDesistenciaForm
    success_url = reverse_lazy('consulta-list')
    permission_required = 'principais.add_altadesistencia'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        try:
            terapeuta_user = TerapeutaUser.objects.get(usuario=self.request.user)
            terapeuta = terapeuta_user.terapeuta
            
            form.fields['fk_terapeuta'].initial = terapeuta.pk_terapeuta
            form.fields['fk_terapeuta'].widget.attrs.update({
                'readonly': 'readonly',
                'style': 'pointer-events: none; background-color: #343a40 !important; color: #ffffff !important; border-color: #495057 !important;'
            })
            form.fields['fk_terapeuta'].queryset = form.fields['fk_terapeuta'].queryset.filter(pk=terapeuta.pk_terapeuta)
            
        except TerapeutaUser.DoesNotExist:
            pass
        
        return form
    
    def form_valid(self, form):
        altadesistencia = form.save(commit=False)
        
        try:
            terapeuta_user = TerapeutaUser.objects.get(usuario=self.request.user)
            altadesistencia.fk_terapeuta = terapeuta_user.terapeuta
        except TerapeutaUser.DoesNotExist:
            if not altadesistencia.fk_terapeuta:
                messages.error(self.request, 'Erro: Terapeuta não foi definido corretamente.')
                return self.form_invalid(form)
        
        altadesistencia.save()
        messages.success(self.request, 'Alta/Desistência cadastrada com sucesso!')
        
        return super().form_valid(form)


# ✅ API VIEWS OTIMIZADAS
class ConsultaListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.ConsultaSerializer
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: Buscar dados relacionados nas APIs
        return models.Consulta.objects.select_related(
            'fk_terapeuta',
            'fk_paciente',
            'fk_terapeuta__fk_abordagem',
            'fk_terapeuta__fk_clinica'
        )


class ConsultaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ConsultaSerializer
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    
    def get_queryset(self):
        return models.Consulta.objects.select_related(
            'fk_terapeuta',
            'fk_paciente',
            'fk_terapeuta__fk_abordagem',
            'fk_terapeuta__fk_clinica'
        )


class TerapeutaListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    serializer_class = serializers.TerapeutaSerializer
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: Buscar dados relacionados + estatísticas
        return models.Terapeuta.objects.select_related(
            'fk_abordagem',
            'fk_clinica'
        ).annotate(
            total_consultas=Count('consulta'),
            total_pacientes=Count('consulta__fk_paciente', distinct=True)
        )


class TerapeutaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    serializer_class = serializers.TerapeutaSerializer
    
    def get_queryset(self):
        return models.Terapeuta.objects.select_related(
            'fk_abordagem',
            'fk_clinica'
        ).annotate(
            total_consultas=Count('consulta'),
            total_pacientes=Count('consulta__fk_paciente', distinct=True)
        )


# Manter as outras API Views como estavam, mas adicionar select_related onde necessário
class DecanoListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Decano.objects.all()
    serializer_class = serializers.DecanoSerializer


class DecanoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Decano.objects.all()
    serializer_class = serializers.DecanoSerializer


class PacienteListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Paciente.objects.all()
    serializer_class = serializers.PacienteSerializer


class PacienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Paciente.objects.all()
    serializer_class = serializers.PacienteSerializer


class AvaliacaoListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Avaliacao.objects.select_related('fk_terapeuta', 'fk_paciente')
    serializer_class = serializers.AvaliacaoSerializer


class AvaliacaoRetrieveUpdateDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Avaliacao.objects.select_related('fk_terapeuta', 'fk_paciente')
    serializer_class = serializers.AvaliacaoSerializer


class AltadesistenciaListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Altadesistencia.objects.select_related('fk_terapeuta', 'fk_paciente')
    serializer_class = serializers.AltadesistenciaSerializer


class AltadesistenciaRetrieveUpdateDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Altadesistencia.objects.select_related('fk_terapeuta', 'fk_paciente')
    serializer_class = serializers.AltadesistenciaSerializer