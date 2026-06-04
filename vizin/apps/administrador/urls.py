from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    path('registro/', views.registro_administrador, name='registro'),
    path('login/', views.login_administrador, name='login'),
    path('painel/', views.painel_adm, name='painel'),

    # Rotas para gerenciamento de funcionários (migradas do app funcionario)
    path('funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('funcionarios/novo/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
]
