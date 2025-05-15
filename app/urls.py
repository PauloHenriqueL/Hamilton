from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),


    path('api/v1/', include('abordagem.urls')),
    path('api/v1/', include('authentication.urls')),
    path('api/v1/', include('captacao.urls')),
    path('api/v1/', include('clinicas.urls')),
    path('api/v1/', include('consulta.urls')),
    path('api/v1/', include('decano.urls')),
    path('api/v1/', include('modalidades.urls')),
    path('api/v1/', include('nucleo.urls')),
    path('api/v1/', include('paciente.urls')),
    path('api/v1/', include('prefeidades.urls')),
    path('api/v1/', include('terapeuta.urls')),
    path('api/v1/', include('avalicao.urls')),
    path('api/v1/', include('associado.urls')),
]
