from django.urls import path
from . import views

urlpatterns = [
    path('associado/list/', views.AssociadoListView.as_view(), name='associado-list'),
    path('associado/create/', views.AssociadoCreateView.as_view(), name='associado-create'),
    path('associado/<int:pk>/detail/', views.AssociadoDetailView.as_view(), name='associado-detail'),
    path('associado/<int:pk>/update/', views.AssociadoUpdateView.as_view(), name='associado-update'),
    path('associado/<int:pk>/delete/', views.AssociadoDeleteView.as_view(), name='associado-delete'),

    # API URLs
    path('api/v1/associado/', views.AssociadoCreateListAPIView.as_view(), name='associado-create-list-api-view'),
    path('api/v1/associado/list/', views.AssociadoCreateListAPIView.as_view(), name='associado-list-api-view'),  # Adicionada esta URL
    path('api/v1/associado/<int:pk>/', views.AssociadoRetrieveUpdateDestroyAPIView.as_view(), name='associado-detail-api-view'),
]