from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers




class AssociadoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = models.Associado
    template_name = 'associado_list.html'
    context_object_name = 'associados'
    paginate_by = 10
    permission_required = 'associado.view_associado'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('nome')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class AssociadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Associado
    template_name = 'associado_create.html'
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('associado-list')
    permission_required = 'associado.add_associado'


class AssociadoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Associado
    template_name = 'associado_detail.html'
    permission_required = 'associado.view_associado'


class AssociadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Associado
    template_name = 'associado_update.html'
    form_class = forms.AssociadoForm
    success_url = reverse_lazy('associado-list')
    permission_required = 'associado.change_associado'


class AssociadoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Associado
    template_name = 'associado_delete.html'
    success_url = reverse_lazy('associado-list')
    permission_required = 'associado.delete_associado'


class AssociadoCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.Associado.objects.all()
    serializer_class = serializers.AssociadoSerializer


class AssociadoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Associado.objects.all()
    serializer_class = serializers.AssociadoSerializer