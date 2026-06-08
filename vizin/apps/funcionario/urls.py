from django.urls import path
from . import views

app_name = 'funcionario'

urlpatterns = [
    path('', views.lista_funcionarios, name='lista_funcionarios'),
    path('novo/', views.cadastrar_funcionario, name='cadastrar_funcionario'),

    # Login/painel do funcionário
    path('login/', views.login_funcionario, name='login'),
    path('painel/', views.painel_funcionario, name='painel'),
]
