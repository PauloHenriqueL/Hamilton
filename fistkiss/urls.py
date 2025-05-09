from django.urls import path
from . import views


urlpatterns = [
    path('firstkiss', views.RegistroCreateListView.as_view(), name='firstkiss-list'),
    path('firstkiss/<int:pk>', views.RegistroRetrieveUpdateDestoyView.as_view(), name='firstkiss-update'),
]
