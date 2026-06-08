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
    path('funcionarios/<int:id>/deletar/', views.deletar_funcionario, name='deletar_funcionario'),

    # Rotas para gerenciamento de moradores
    path('moradores/', views.lista_moradores, name='lista_moradores'),
    path('moradores/novo/', views.cadastrar_morador, name='cadastrar_morador'),
    path('moradores/<int:id>/editar/', views.editar_morador, name='editar_morador'),
    path('moradores/<int:id>/deletar/', views.deletar_morador, name='deletar_morador'),
]
