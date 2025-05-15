from django.urls import path
from . import views

urlpatterns = [
    # Views para templates HTML
    path('avaliacao/list/', views.AvaliacaoListView.as_view(), name='avaliacao-list'),
    path('avaliacao/create/', views.AvaliacaoCreateView.as_view(), name='avaliacao-create'),
    path('avaliacao/<int:pk>/detail/', views.AvaliacaoDetailView.as_view(), name='avaliacao-detail'),
    path('avaliacao/<int:pk>/update/', views.AvaliacaoUpdateView.as_view(), name='avaliacao-update'),
    path('avaliacao/<int:pk>/delete/', views.AvaliacaoDeleteView.as_view(), name='avaliacao-delete'),

    # API URLs - simplificando para evitar conflitos
    path('api/v1/avaliacoes/', views.AvaliacaoCreateListAPIView.as_view(), name='avaliacao-api-list-create'),
    path('api/v1/avaliacoes/<int:pk>/', views.AvaliacaoRetrieveUpdateDestroyAPIView.as_view(), name='avaliacao-api-detail'),
]