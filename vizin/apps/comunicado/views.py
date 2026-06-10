from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Comunicado
from .forms import ComunicadoForm

@login_required
def cadastrar_comunicado(request):
    """Permite que um administrador cadastre um novo comunicado."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied

    form = ComunicadoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comunicado = form.save(commit=False)
        comunicado.administrador = request.user.administrador
        comunicado.save()
        messages.success(request, 'Comunicado cadastrado com sucesso.')
        return redirect('comunicado:lista_comunicados')

    return render(request, 'comunicado/cadastrar_comunicado.html', {'form': form})


@login_required
def lista_comunicados(request):
    """Lista comunicados visíveis para o usuário logado (Admin, Morador ou Funcionário)."""
    admin = None
    if hasattr(request.user, 'administrador'):
        admin = request.user.administrador
    elif hasattr(request.user, 'morador'):
        admin = request.user.morador.administrador
    elif hasattr(request.user, 'funcionario'):
        admin = request.user.funcionario.administrador
    else:
        raise PermissionDenied

    comunicados_list = Comunicado.objects.filter(administrador=admin).order_by('-data')
    
    paginator = Paginator(comunicados_list, 10) # 10 por página
    page = request.GET.get('page')
    try:
        comunicados = paginator.page(page)
    except PageNotAnInteger:
        comunicados = paginator.page(1)
    except EmptyPage:
        comunicados = paginator.page(paginator.num_pages)

    return render(request, 'comunicado/lista_comunicados.html', {'comunicados': comunicados})


@login_required
def editar_comunicado(request, id):
    """Permite que um administrador edite um comunicado existente."""
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied

    comunicado = get_object_or_404(Comunicado, id=id, administrador=request.user.administrador)
    form = ComunicadoForm(request.POST or None, instance=comunicado)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Comunicado atualizado com sucesso.')
        return redirect('comunicado:lista_comunicados')

    return render(request, 'comunicado/editar_comunicado.html', {'form': form, 'comunicado': comunicado})


@login_required
def deletar_comunicado(request, id):
    """Deleta um comunicado. Retorna JSON."""
    if not hasattr(request.user, 'administrador'):
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido.'}, status=405)

    comunicado = get_object_or_404(Comunicado, id=id, administrador=request.user.administrador)
    comunicado.delete()

    return JsonResponse({'ok': True})
