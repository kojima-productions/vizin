from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import PermissionDenied

from .forms import AdministradorRegistrationForm, AdministradorLoginForm
from .models import Administrador
from django.contrib.auth.models import User


def registro_administrador(request):
    """View para cadastro tradicional de Administrador.

    Fluxo:
    - GET: exibe o formulário
    - POST: valida o formulário, cria User com create_user() dentro de transaction.atomic(), cria Administrador e redireciona para login.
    """
    form = None
    if request.method == 'POST':
        form = AdministradorRegistrationForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            with transaction.atomic():
                user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
                Administrador.objects.create(user=user, cpf=cpf)
            return redirect('administrador:login')
    else:
        form = AdministradorRegistrationForm()
    return render(request, 'administrador/registro.html', {'form': form})


def login_administrador(request):
    """View para login tradicional de Administrador.

    - Autentica via email+senha
    - Checa se o User tem Administrador vinculado; se não, adiciona erro e nega acesso
    - Em sucesso, faz login() e redireciona para painel
    """
    form = None
    if request.method == 'POST':
        form = AdministradorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=email, password=senha)
            if user is not None:
                if hasattr(user, 'administrador'):
                    login(request, user)
                    return redirect('administrador:painel')
                else:
                    form.add_error(None, 'Usuário autenticado não possui perfil de Administrador.')
            else:
                form.add_error(None, 'Credenciais inválidas.')
    else:
        form = AdministradorLoginForm()
    return render(request, 'administrador/login.html', {'form': form})


@login_required
def painel_adm(request):
    """Painel do Administrador. Exige login e perfil Administrador."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied
    return render(request, 'administrador/painel.html')
