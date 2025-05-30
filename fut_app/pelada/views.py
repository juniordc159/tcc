from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Pelada
from pelada.repository.pelada_repository import PeladaRepository
from pelada.service.pelada_service import PeladaService
from pelada.repository.participante_pelada_repository import ParticipantePeladaRepository
from pelada.service.participante_pelada_service import ParticipantePeladaService

def pelada_factory():
    pelada_repo = PeladaRepository()
    pelada_service = PeladaService(pelada_repo)

    return pelada_service
def participante_factory():
    participante_repo = ParticipantePeladaRepository()
    participante_service = ParticipantePeladaService(participante_repo)

    return participante_service

# Create your views here.
@login_required
def gerenciador(request):
    pelada_usecase = pelada_factory()
    peladas = pelada_usecase.listar_peladas(request.user.id)
    return render(request, 'pelada/gerenciador.html', {'peladas': peladas})

@login_required
def cadastra_pelada(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('desc')


        if not all([nome,descricao]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return render(request, 'pelada/cria_pelada.html')
        pelada_usecase = pelada_factory()
        pelada_usecase.criar_ou_editar_pelada(
            Pelada(
                criador=request.user,
                nome=nome,
                descricao=descricao,
            ))
        return redirect('gerenciador')

    return render(request, 'pelada/cria_pelada.html')

@login_required
def editar_pelada(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id, criador=request.user)
    players_usercase = participante_factory()
    players = players_usercase.participante_pelada_repository.get_participantes_by_pelada_id(pelada_id)
    return render(request, 'pelada/editar_pelada.html', {'pelada': pelada, 'players': players})

@login_required
def salva_pelada(request, pelada_id):
    pelada_usecase = pelada_factory()
    if request.method == 'POST':

        return redirect('gerenciador')

    return render(request, 'pelada/editar_pelada.html', {'pelada': pelada_id})


@login_required
def excluir_pelada(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id, criador=request.user)
    if request.method == 'POST':
        pelada.delete()
        return redirect('gerenciador')