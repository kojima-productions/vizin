from django.urls import path
from . import views

app_name = 'funcionario'

urlpatterns = [
    path('', views.lista_funcionarios, name='lista_funcionarios'),
    path('novo/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
]
