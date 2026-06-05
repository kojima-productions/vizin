from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def cadastrar_funcionario(request):
    # rotas movidas para apps.administrador.views
    return redirect('administrador:cadastrar_funcionario')


@login_required
def lista_funcionarios(request):
    # rotas movidas para apps.administrador.views
    return redirect('administrador:lista_funcionarios')
