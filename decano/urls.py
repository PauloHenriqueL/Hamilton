from django.urls import path
from . import views


urlpatterns = [
    path('decano', views.DecanoCreateListView.as_view(), name='decano-list'),
    path('decano/<int:pk>', views.DecanoRetrieveUpdateDestoyView.as_view(), name='decano-update'),
]
