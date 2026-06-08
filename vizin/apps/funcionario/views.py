from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import FuncionarioLoginForm


@login_required
def cadastrar_funcionario(request):
    # rotas movidas para apps.administrador.views
    return redirect('administrador:cadastrar_funcionario')


@login_required
def lista_funcionarios(request):
    # rotas movidas para apps.administrador.views
    return redirect('administrador:lista_funcionarios')


def login_funcionario(request):
    """View para login de Funcionário.

    - GET: mostra o formulário
    - POST: valida, autentica por email+senha e checa perfil Funcionario
    """
    form = FuncionarioLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login_val = form.cleaned_data.get('login')
        senha = form.cleaned_data.get('senha')

        user = authenticate(request, username=login_val, password=senha)

        if user is not None:
            if hasattr(user, 'funcionario'):
                login(request, user)
                return redirect('funcionario:painel')
            else:
                form.add_error(None, 'Usuário autenticado não possui perfil de Funcionário.')
        else:
            form.add_error(None, 'Credenciais inválidas.')

    return render(request, 'funcionario/login.html', {'form': form})


@login_required
def painel_funcionario(request):
    """Painel do Funcionário. Exige login e perfil Funcionario."""
    if not hasattr(request.user, 'funcionario'):
        raise PermissionDenied
    return render(request, 'funcionario/painel.html')
