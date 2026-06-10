from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest

from .forms import AdministradorRegistrationForm, AdministradorLoginForm
from .models import Administrador
from django.contrib.auth.models import User
from apps.funcionario.models import Funcionario
from apps.funcionario.forms import FuncionarioForm, FuncionarioEditForm
from apps.morador.forms import MoradorForm, MoradorEditForm
from apps.morador.models import Morador, Apartamento
from apps.area.models import Area
from apps.area.forms import AreaForm


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


@login_required
def cadastrar_funcionario(request):
    """Permite que um administrador cadastre um funcionário.

    Mantém o mesmo fluxo original: validação do form, criação de User e Funcionario dentro de uma transação.
    """
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied

    form = FuncionarioForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        dados = form.cleaned_data
        with transaction.atomic():
            user = User.objects.create_user(
                username=dados['email'],
                email=dados['email'],
                password=dados['senha'],
                first_name=dados['nome'],
            )
            Funcionario.objects.create(
                user=user,
                cpf=dados['cpf'],
                cargo=dados['cargo'],
                telefone=dados['telefone'],
                administrador=request.user.administrador,
            )
        messages.success(request, 'Funcionário cadastrado com sucesso.')
        return redirect('administrador:lista_funcionarios')

    return render(request, 'administrador/cadastrar_funcionario.html', {'form': form})


@login_required
def editar_funcionario(request, id):
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied

    funcionario = get_object_or_404(Funcionario, id=id, administrador=request.user.administrador)
    
    if request.method == 'POST':
        form = FuncionarioEditForm(request.POST, funcionario_id=id)
        if form.is_valid():
            dados = form.cleaned_data
            
            with transaction.atomic():
                # Atualizar User
                user = funcionario.user
                user.username = dados['email']
                user.email = dados['email']
                user.first_name = dados['nome']
                if dados.get('senha'):
                    user.set_password(dados['senha'])
                user.save()
                
                # Atualizar Funcionario
                funcionario.cpf = dados['cpf']
                funcionario.telefone = dados['telefone']
                funcionario.cargo = dados['cargo']
                funcionario.save()
                
            messages.success(request, 'Dados do funcionário atualizados com sucesso.')
            return redirect('administrador:lista_funcionarios')
    else:
        # Preencher formulário com dados atuais
        initial_data = {
            'nome': funcionario.user.first_name,
            'email': funcionario.user.email,
            'cpf': funcionario.cpf,
            'telefone': funcionario.telefone,
            'cargo': funcionario.cargo,
        }
        form = FuncionarioEditForm(initial=initial_data, funcionario_id=id)

    return render(request, 'administrador/editar_funcionario.html', {'form': form, 'funcionario': funcionario})


@login_required
def lista_funcionarios(request):
    """Lista funcionários do administrador logado."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied
    funcionarios = Funcionario.objects.filter(administrador=request.user.administrador).select_related('user')
    return render(request, 'administrador/lista_funcionarios.html', {'funcionarios': funcionarios})



@login_required
def cadastrar_morador(request):
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied

    form = MoradorForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        dados = form.cleaned_data
        bloco = dados.get('bloco')
        andar = dados.get('andar')
        numero = dados.get('numero')

        with transaction.atomic():
            apartamento, created = Apartamento.objects.get_or_create(
                bloco=bloco,
                andar=andar,
                numero=numero,
            )

            user = User.objects.create_user(
                username=dados['email'],
                email=dados['email'],
                password=dados['senha'],
                first_name=dados['nome'],
            )

            Morador.objects.create(
                user=user,
                cpf=dados['cpf'],
                telefone=dados['telefone'],
                tipo_morador=dados['tipo_morador'],
                administrador=request.user.administrador,
                apartamento=apartamento,
            )

        messages.success(request, 'Morador cadastrado com sucesso.')
        return redirect('administrador:lista_moradores')

    return render(request, 'administrador/cadastrar_morador.html', {'form': form})


@login_required
def editar_morador(request, id):
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied

    morador = get_object_or_404(Morador, id=id, administrador=request.user.administrador)
    
    if request.method == 'POST':
        form = MoradorEditForm(request.POST, morador_id=id)
        if form.is_valid():
            dados = form.cleaned_data
            
            with transaction.atomic():
                # Atualizar Apartamento
                apartamento, created = Apartamento.objects.get_or_create(
                    bloco=dados['bloco'],
                    andar=dados['andar'],
                    numero=dados['numero'],
                )
                
                # Atualizar User
                user = morador.user
                user.username = dados['email']
                user.email = dados['email']
                user.first_name = dados['nome']
                if dados.get('senha'):
                    user.set_password(dados['senha'])
                user.save()
                
                # Atualizar Morador
                morador.cpf = dados['cpf']
                morador.telefone = dados['telefone']
                morador.tipo_morador = dados['tipo_morador']
                morador.apartamento = apartamento
                morador.save()
                
            messages.success(request, 'Dados do morador atualizados com sucesso.')
            return redirect('administrador:lista_moradores')
    else:
        # Preencher formulário com dados atuais
        initial_data = {
            'nome': morador.user.first_name,
            'email': morador.user.email,
            'cpf': morador.cpf,
            'telefone': morador.telefone,
            'tipo_morador': morador.tipo_morador,
            'bloco': morador.apartamento.bloco,
            'andar': morador.apartamento.andar,
            'numero': morador.apartamento.numero,
        }
        form = MoradorEditForm(initial=initial_data, morador_id=id)

    return render(request, 'administrador/editar_morador.html', {'form': form, 'morador': morador})


@login_required
def lista_moradores(request):
    """Lista moradores do administrador logado."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied
    moradores = Morador.objects.filter(administrador=request.user.administrador).select_related('user', 'apartamento')
    return render(request, 'administrador/lista_moradores.html', {'moradores': moradores})


@login_required
def deletar_morador(request, id):
    """Deleta um morador pertencente ao administrador logado. Retorna JSON."""
    if not hasattr(request.user, 'administrador'):
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    morador = get_object_or_404(Morador, id=id, administrador=request.user.administrador)

    # Proteção: não permitir que o administrador delete o próprio usuário
    if morador.user == request.user:
        return JsonResponse({'error': 'Não é possível deletar o próprio usuário.'}, status=400)

    # Deletar o User associado — modelos provavelmente configurados para cascade
    morador.user.delete()

    return JsonResponse({'ok': True})


@login_required
def deletar_funcionario(request, id):
    """Deleta um funcionário pertencente ao administrador logado. Retorna JSON."""
    if not hasattr(request.user, 'administrador'):
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    funcionario = get_object_or_404(Funcionario, id=id, administrador=request.user.administrador)

    # Proteção: não permitir que o administrador delete o próprio usuário
    if funcionario.user == request.user:
        return JsonResponse({'error': 'Não é possível deletar o próprio usuário.'}, status=400)

    # Deletar o User associado — modelos provavelmente configurados para cascade
    funcionario.user.delete()

    return JsonResponse({'ok': True})


@login_required
def lista_areas(request):
    """Lista áreas comuns do administrador logado."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied
    areas = Area.objects.filter(administrador=request.user.administrador)
    return render(request, 'administrador/lista_areas.html', {'areas': areas})


@login_required
def cadastrar_area(request):
    """Cadastra uma nova área comum."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied

    form = AreaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        area = form.save(commit=False)
        area.administrador = request.user.administrador
        area.save()
        messages.success(request, 'Área comum cadastrada com sucesso.')
        return redirect('administrador:lista_areas')

    return render(request, 'administrador/cadastrar_area.html', {'form': form})


@login_required
def editar_area(request, id):
    """Edita uma área comum existente."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied

    area = get_object_or_404(Area, id=id, administrador=request.user.administrador)
    form = AreaForm(request.POST or None, instance=area)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Área comum atualizada com sucesso.')
        return redirect('administrador:lista_areas')

    return render(request, 'administrador/editar_area.html', {'form': form, 'area': area})


@login_required
def deletar_area(request, id):
    """Deleta uma área comum. Retorna JSON."""
    if not hasattr(request.user, 'administrador'):
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    area = get_object_or_404(Area, id=id, administrador=request.user.administrador)
    area.delete()

    return JsonResponse({'ok': True})


@login_required
def lista_reservas(request):
    """Lista todas as solicitações de reserva para o administrador."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied
    
    # Filtra reservas das áreas gerenciadas por este administrador
    reservas = Reserva.objects.filter(administrador=request.user.administrador).order_by('status', 'horario_inicio')
    
    # Filtro simples via GET se necessário (ex: ?status=aberto)
    status_filtro = request.GET.get('status')
    if status_filtro:
        reservas = reservas.filter(status=status_filtro)

    return render(request, 'administrador/lista_reservas.html', {
        'reservas': reservas,
        'status_choices': Reserva.Status.choices
    })


@login_required
def validar_reserva(request, reserva_id):
    """Aprova ou nega uma reserva. Retorna JSON."""
    if not hasattr(request.user, 'administrador'):
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    reserva = get_object_or_404(Reserva, id=reserva_id, administrador=request.user.administrador)
    
    # Ação pode ser 'aprovar' ou 'negar'
    import json
    data = json.loads(request.body)
    acao = data.get('acao')

    if acao == 'aprovar':
        reserva.status = Reserva.Status.APROVADO
    elif acao == 'negar':
        reserva.status = Reserva.Status.NEGADO
    else:
        return JsonResponse({'error': 'Ação inválida.'}, status=400)

    reserva.save()
    return JsonResponse({'ok': True, 'novo_status': reserva.get_status_display()})

