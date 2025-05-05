from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('abordagem.urls')),
    path('api/v1/', include('authentication.urls')),  # Inclui as URLs do app 'authentication'
    path('api/v1/', include('captacao.urls')),
    path('api/v1/', include('clinicas.urls')),
    path('api/v1/', include('decano.urls')),
    path('api/v1/', include('modalidades.urls')),
    path('api/v1/', include('nucleo.urls')),
    path('api/v1/', include('paciente.urls')),
    path('api/v1/', include('prefeidades.urls')),
    path('api/v1/', include('terapeuta.urls')),
]
