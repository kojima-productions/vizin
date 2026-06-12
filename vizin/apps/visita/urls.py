from django.urls import path
from . import views

app_name = 'visita'

urlpatterns = [
    path('cadastrar/', views.cadastrar_visita, name='cadastrar_visita'),
    path('minhas-visitas/', views.lista_visitas_morador, name='lista_visitas_morador'),
    path('gerenciar/', views.lista_visitas_func, name='lista_visitas_func'),
    path('registrar/<int:pk>/', views.registrar_entrada, name='registrar_entrada'),
    path('relatorio/', views.lista_visitas_adm, name='lista_visitas_adm'),
]
