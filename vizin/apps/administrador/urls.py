from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    path('registro/', views.registro_administrador, name='registro'),
    path('login/', views.login_administrador, name='login'),
    path('painel/', views.painel_adm, name='painel'),
]
