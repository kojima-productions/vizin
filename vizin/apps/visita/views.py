from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Visita
from .forms import VisitaForm
from apps.morador.models import Morador
from apps.funcionario.models import Funcionario
from apps.administrador.models import Administrador

@login_required
def cadastrar_visita(request):
    if not hasattr(request.user, 'morador'):
        messages.error(request, "Acesso restrito a moradores.")
        return redirect('index')
    
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.morador = request.user.morador
            visita.save()
            messages.success(request, f"Visita agendada com sucesso! Código de acesso: {visita.acesso}")
            return redirect('visita:lista_visitas_morador')
    else:
        form = VisitaForm()
    
    return render(request, 'morador/cadastrar_visita.html', {'form': form})

@login_required
def lista_visitas_morador(request):
    if not hasattr(request.user, 'morador'):
        messages.error(request, "Acesso restrito a moradores.")
        return redirect('index')
    
    visitas_list = Visita.objects.filter(morador=request.user.morador).order_by('-data_criacao')
    paginator = Paginator(visitas_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'morador/lista_visitas.html', {'page_obj': page_obj})

@login_required
def lista_visitas_func(request):
    if not hasattr(request.user, 'funcionario') and not hasattr(request.user, 'administrador'):
        messages.error(request, "Acesso restrito a funcionários ou administradores.")
        return redirect('index')
    
    if hasattr(request.user, 'funcionario'):
        adm = request.user.funcionario.administrador
    else:
        adm = request.user.administrador

    query = request.GET.get('q', '')
    visitas_list = Visita.objects.filter(morador__administrador=adm).order_by('-data_criacao')
    
    if query:
        visitas_list = visitas_list.filter(
            Q(acesso__icontains=query) | 
            Q(cpf__icontains=query) | 
            Q(nome__icontains=query)
        )
    
    paginator = Paginator(visitas_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'funcionario/lista_visitas.html', {
        'page_obj': page_obj,
        'query': query
    })

@login_required
def registrar_entrada(request, pk):
    if not hasattr(request.user, 'funcionario') and not hasattr(request.user, 'administrador'):
        messages.error(request, "Acesso restrito.")
        return redirect('index')
    
    if hasattr(request.user, 'funcionario'):
        adm = request.user.funcionario.administrador
    else:
        adm = request.user.administrador

    visita = get_object_or_404(Visita, pk=pk, morador__administrador=adm)
    
    if request.method == 'POST':
        if visita.status == Visita.StatusVisita.AGENDADA:
            visita.status = Visita.StatusVisita.REGISTRADA
            visita.data_entrada = timezone.now()
            # Se for funcionário, associa. Se for adm, pode ficar nulo ou associar se houver perfil func
            if hasattr(request.user, 'funcionario'):
                visita.funcionario = request.user.funcionario
            visita.save()
            messages.success(request, f"Entrada de {visita.nome} registrada com sucesso!")
        else:
            messages.warning(request, "Esta visita já foi registrada anteriormente.")
            
    return redirect('visita:lista_visitas_func')

@login_required
def lista_visitas_adm(request):
    if not hasattr(request.user, 'administrador'):
        messages.error(request, "Acesso restrito a administradores.")
        return redirect('index')
    
    # Administrador vê apenas visitas do seu condomínio
    adm = request.user.administrador
    visitas_list = Visita.objects.filter(morador__administrador=adm).order_by('-data_criacao')
    
    query = request.GET.get('q', '')
    if query:
        visitas_list = visitas_list.filter(
            Q(acesso__icontains=query) | 
            Q(cpf__icontains=query) | 
            Q(nome__icontains=query)
        )
        
    paginator = Paginator(visitas_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'administrador/lista_visitas.html', {
        'page_obj': page_obj,
        'query': query
    })
