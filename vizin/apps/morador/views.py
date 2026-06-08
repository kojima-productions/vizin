from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .forms import MoradorLoginForm
from .models import Morador


def login_morador(request):
    """View para login de Morador.

    Fluxo:
    - GET: renderiza o formulário
    - POST: valida o formulário, autentica via email+senha (username=email)
      e verifica se o User possui o profile Morador antes de realizar login.

    Em caso de sucesso redireciona para a view de painel do morador.
    """
    form = MoradorLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login_val = form.cleaned_data.get('login')
        senha = form.cleaned_data.get('senha')

        # Autentica (projeto usa username igual ao email ao criar usuários)
        user = authenticate(request, username=login_val, password=senha)

        if user is not None:
            # Verifica se este user tem um perfil Morador associado
            if hasattr(user, 'morador'):
                login(request, user)
                return redirect('morador:painel')
            else:
                form.add_error(None, 'Usuário autenticado não possui perfil de Morador.')
        else:
            form.add_error(None, 'Credenciais inválidas.')

    return render(request, 'morador/login.html', {'form': form})


@login_required
def painel_morador(request):
    """Painel do Morador. Exige login e perfil Morador."""
    if not hasattr(request.user, 'morador'):
        raise PermissionDenied
    return render(request, 'morador/painel.html')
