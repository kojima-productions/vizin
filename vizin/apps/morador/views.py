from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse

from .forms import MoradorLoginForm, VeiculoForm
from .models import Morador, Veiculo
from apps.area.models import Area, Reserva
from apps.area.forms import ReservaForm


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


@login_required
def lista_areas_comuns(request):
    """Lista áreas comuns disponíveis para reserva."""
    if not hasattr(request.user, 'morador'):
        raise PermissionDenied
    
    # Áreas do administrador do morador
    areas = Area.objects.filter(administrador=request.user.morador.administrador)
    return render(request, 'morador/lista_areas.html', {'areas': areas})


@login_required
def fazer_reserva(request, area_id):
    """Realiza a reserva de uma área."""
    if not hasattr(request.user, 'morador'):
        raise PermissionDenied
    
    area = get_object_or_404(Area, id=area_id, administrador=request.user.morador.administrador)
    form = ReservaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        inicio = form.cleaned_data['horario_inicio']
        fim = form.cleaned_data['horario_fim']

        # Validação de conflito de horário
        conflito = Reserva.objects.filter(
            area=area,
            horario_inicio__lt=fim,
            horario_fim__gt=inicio
        ).exists()

        if conflito:
            form.add_error(None, "Já existe uma reserva para esta área no horário selecionado.")
        else:
            reserva = form.save(commit=False)
            reserva.area = area
            reserva.morador = request.user.morador
            reserva.administrador = area.administrador
            reserva.save()
            messages.success(request, f'Reserva para {area.nome} realizada com sucesso!')
            return redirect('morador:minhas_reservas')

    return render(request, 'morador/fazer_reserva.html', {'form': form, 'area': area})


@login_required
def minhas_reservas(request):
    """Lista as reservas do morador logado."""
    if not hasattr(request.user, 'morador'):
        raise PermissionDenied
    
    reservas = Reserva.objects.filter(morador=request.user.morador).order_by('-horario_inicio')
    return render(request, 'morador/minhas_reservas.html', {'reservas': reservas})


@login_required
def cancelar_reserva(request, reserva_id):
    """Cancela uma reserva do morador."""
    if not hasattr(request.user, 'morador'):
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    reserva = get_object_or_404(Reserva, id=reserva_id, morador=request.user.morador)
    reserva.delete()
    return JsonResponse({'ok': True})


@login_required
def gerenciar_veiculo(request):
    """Permite que o morador cadastre ou edite o veículo do seu apartamento."""
    if not hasattr(request.user, 'morador'):
        raise PermissionDenied
    
    morador = request.user.morador
    apartamento = morador.apartamento
    
    # Tenta obter o veículo do apartamento
    try:
        veiculo = apartamento.veiculo
    except Veiculo.DoesNotExist:
        veiculo = None

    form = VeiculoForm(request.POST or None, instance=veiculo)

    if request.method == 'POST' and form.is_valid():
        novo_veiculo = form.save(commit=False)
        novo_veiculo.apartamento = apartamento
        novo_veiculo.save()
        messages.success(request, 'Informações do veículo salvas com sucesso!')
        return redirect('morador:painel')

    return render(request, 'morador/gerenciar_veiculo.html', {
        'form': form,
        'veiculo': veiculo
    })


@login_required
def deletar_veiculo_morador(request):
    """Permite que o morador exclua o veículo do seu apartamento."""
    if not hasattr(request.user, 'morador'):
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    try:
        veiculo = request.user.morador.apartamento.veiculo
        veiculo.delete()
        return JsonResponse({'ok': True})
    except Veiculo.DoesNotExist:
        return JsonResponse({'error': 'Veículo não encontrado.'}, status=404)
