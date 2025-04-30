from django.urls import path
from . import views


urlpatterns = [
    path('nucleo', views.NucleoCreateListView.as_view(), name='nucleo-list'),
    path('nucleo/<int:pk>', views.NucleoRetrieveUpdateDestoyView.as_view(), name='nucleo-update'),
]
