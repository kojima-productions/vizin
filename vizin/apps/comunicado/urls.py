from django.urls import path
from . import views

app_name = 'comunicado'

urlpatterns = [
    path('', views.lista_comunicados, name='lista_comunicados'),
    path('novo/', views.cadastrar_comunicado, name='cadastrar_comunicado'),
    path('<int:id>/editar/', views.editar_comunicado, name='editar_comunicado'),
    path('<int:id>/deletar/', views.deletar_comunicado, name='deletar_comunicado'),
]
