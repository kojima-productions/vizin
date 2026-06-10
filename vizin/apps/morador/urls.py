from django.urls import path
from . import views

app_name = 'morador'

urlpatterns = [
    path('login/', views.login_morador, name='login'),
    path('painel/', views.painel_morador, name='painel'),
    
    # Rotas para reserva de áreas
    path('areas/', views.lista_areas_comuns, name='lista_areas_comuns'),
    path('areas/<int:area_id>/reservar/', views.fazer_reserva, name='fazer_reserva'),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('reservas/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),

    # Rotas para veículos
    path('meu-veiculo/', views.gerenciar_veiculo, name='gerenciar_veiculo'),
    path('meu-veiculo/deletar/', views.deletar_veiculo_morador, name='deletar_veiculo'),

    # Rotas para reclamações
    path('reclamacoes/', views.lista_reclamacoes, name='lista_reclamacoes'),
    path('reclamacoes/nova/', views.cadastrar_reclamacao, name='cadastrar_reclamacao'),
    path('reclamacoes/<int:id>/deletar/', views.deletar_reclamacao, name='deletar_reclamacao'),
]
