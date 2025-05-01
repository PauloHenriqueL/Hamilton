from django.urls import path
from . import views


urlpatterns = [
    path('captacao', views.CaptacaoCreateListView.as_view(), name='captacao-list'),
    path('captacao/<int:pk>', views.CaptacaoRetrieveUpdateDestoyView.as_view(), name='captacao-update'),
]
