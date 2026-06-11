from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from .models import Encomenda
from .forms import EncomendaForm

@login_required
def cadastrar_encomenda(request):
    if not (hasattr(request.user, 'administrador') or hasattr(request.user, 'funcionario')):
        raise PermissionDenied
    
    administrador = None
    if hasattr(request.user, 'administrador'):
        administrador = request.user.administrador
    elif hasattr(request.user, 'funcionario'):
        administrador = request.user.funcionario.administrador
        
    form = EncomendaForm(request.POST or None, administrador=administrador)
    
    if request.method == 'POST' and form.is_valid():
        encomenda = form.save(commit=False)
        encomenda.registrado_por = request.user
        encomenda.save()
        messages.success(request, 'Encomenda registrada com sucesso.')
        
        if hasattr(request.user, 'administrador'):
            return redirect('encomenda:lista_encomendas_adm')
        return redirect('encomenda:lista_encomendas_func')
        
    # Using the same template for both as they are functionally identical for registration
    return render(request, 'funcionario/cadastrar_encomenda.html', {'form': form})

@login_required
def lista_encomendas_adm(request):
    if not hasattr(request.user, 'administrador'):
        raise PermissionDenied
    
    encomendas = Encomenda.objects.filter(
        apartamento__morador__administrador=request.user.administrador
    ).distinct().order_by('-data_chegada')
    
    return render(request, 'administrador/lista_encomendas.html', {'encomendas': encomendas})

@login_required
def lista_encomendas_func(request):
    if not hasattr(request.user, 'funcionario'):
        raise PermissionDenied
    
    encomendas = Encomenda.objects.filter(
        apartamento__morador__administrador=request.user.funcionario.administrador
    ).distinct().order_by('-data_chegada')
    
    return render(request, 'funcionario/lista_encomendas.html', {'encomendas': encomendas})

@login_required
def lista_encomendas_morador(request):
    if not hasattr(request.user, 'morador'):
        raise PermissionDenied
    
    encomendas = Encomenda.objects.filter(
        apartamento=request.user.morador.apartamento
    ).order_by('-data_chegada')
    
    return render(request, 'morador/lista_encomendas.html', {'encomendas': encomendas})

@login_required
def registrar_entrega(request, pk):
    if not (hasattr(request.user, 'administrador') or hasattr(request.user, 'funcionario')):
        raise PermissionDenied
    
    if request.method != 'POST':
        messages.error(request, 'Método não permitido.')
        if hasattr(request.user, 'administrador'):
            return redirect('encomenda:lista_encomendas_adm')
        return redirect('encomenda:lista_encomendas_func')
        
    administrador = None
    if hasattr(request.user, 'administrador'):
        administrador = request.user.administrador
    elif hasattr(request.user, 'funcionario'):
        administrador = request.user.funcionario.administrador
        
    encomenda = get_object_or_404(Encomenda, pk=pk, apartamento__morador__administrador=administrador)
    
    if encomenda.status == Encomenda.Status.RECEBIDA:
        encomenda.status = Encomenda.Status.ENTREGUE
        encomenda.data_entrega = timezone.now()
        encomenda.entregue_por = request.user
        encomenda.save()
        messages.success(request, 'Entrega registrada com sucesso.')
    
    if hasattr(request.user, 'administrador'):
        return redirect('encomenda:lista_encomendas_adm')
    return redirect('encomenda:lista_encomendas_func')
