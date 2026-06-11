from django.urls import path
from . import views

app_name = 'encomenda'

urlpatterns = [
    path('cadastrar/', views.cadastrar_encomenda, name='cadastrar_encomenda'),
    path('lista/adm/', views.lista_encomendas_adm, name='lista_encomendas_adm'),
    path('lista/func/', views.lista_encomendas_func, name='lista_encomendas_func'),
    path('lista/morador/', views.lista_encomendas_morador, name='lista_encomendas_morador'),
    path('entrega/<int:pk>/', views.registrar_entrega, name='registrar_entrega'),
]
