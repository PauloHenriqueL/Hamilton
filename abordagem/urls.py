from django.urls import path
from . import views


urlpatterns = [
    path('abordagem', views.AbordagemCreateListView.as_view(), name='abordagem-list'),
    path('abordagem/<int:pk>', views.AbordagemRetrieveUpdateDestoyView.as_view(), name='abordagem-update'),
]
