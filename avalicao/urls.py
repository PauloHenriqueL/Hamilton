from django.urls import path
from . import views

urlpatterns = [
    path('avaliacao/list/', views.AvaliacaoListView.as_view(), name='avaliacao-list'),
    path('avaliacao/create/', views.AvaliacaoCreateView.as_view(), name='avaliacao-create'),
    path('avaliacao/<int:pk>/detail/', views.AvaliacaoDetailView.as_view(), name='avaliacao-detail'),
    path('avaliacao/<int:pk>/update/', views.AvaliacaoUpdateView.as_view(), name='avaliacao-update'),
    path('avaliacao/<int:pk>/delete/', views.AvaliacaoDeleteView.as_view(), name='avaliacao-delete'),

    # API URLs
    path('api/v1/avaliacao/', views.AvaliacaoCreateListAPIView.as_view(), name='avaliacao-create-list-api-view'),
    path('api/v1/avaliacao/list/', views.AvaliacaoCreateListAPIView.as_view(), name='avaliacao-list-api-view'),  # Adicionada esta URL
    path('api/v1/avaliacao/<int:pk>/', views.AvaliacaoRetrieveUpdateDestroyAPIView.as_view(), name='avaliacao-detail-api-view'),
]