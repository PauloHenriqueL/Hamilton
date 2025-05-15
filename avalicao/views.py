from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers




class AvaliacaoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Avaliacao
    template_name = 'avaliacao_list.html'
    context_object_name = 'avaliacoes'  # Corrigido: 'avaliacaos' para 'avaliacoes'
    paginate_by = 10
    permission_required = 'avaliacao.view_avaliacao'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros para avaliador e avaliado
        avaliador_id = self.request.GET.get('avaliador')
        avaliado_id = self.request.GET.get('avaliado')

        if avaliador_id:
            queryset = queryset.filter(fk_avaliador__pk=avaliador_id)

        if avaliado_id:
            queryset = queryset.filter(fk_avaliado__pk=avaliado_id)
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona avaliadores e avaliados ao contexto para os filtros
        context['avaliadores'] = models.Avaliador.objects.all()
        context['avaliados'] = models.Avaliado.objects.all()
        return context

class AvaliacaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Avaliacao
    template_name = 'avaliacao_create.html'
    form_class = forms.AvaliacaoForm
    success_url = reverse_lazy('avaliacao-list')
    permission_required = 'avaliacao.add_avaliacao'


class AvaliacaoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Avaliacao
    template_name = 'avaliacao_detail.html'
    permission_required = 'avaliacao.view_avaliacao'


class AvaliacaoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Avaliacao
    template_name = 'avaliacao_update.html'
    form_class = forms.AvaliacaoForm
    success_url = reverse_lazy('avaliacao-list')
    permission_required = 'avaliacao.change_avaliacao'


class AvaliacaoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Avaliacao
    template_name = 'avaliacao_delete.html'
    success_url = reverse_lazy('avaliacao-list')
    permission_required = 'avaliacao.delete_avaliacao'


class AvaliacaoCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.Avaliacao.objects.all()
    serializer_class = serializers.AvaliacaoSerializer


class AvaliacaoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Avaliacao.objects.all()
    serializer_class = serializers.AvaliacaoSerializer