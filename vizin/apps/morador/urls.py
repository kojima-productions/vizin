from django.urls import path
from . import views

app_name = 'morador'

urlpatterns = [
    path('login/', views.login_morador, name='login'),
    path('painel/', views.painel_morador, name='painel'),
]
