from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from urllib.parse import parse_qs
from pelada.models import ParticipantePelada, Pelada
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
    pelada = pelada_usecase.pelada_repository.get_pelada_by_id(pelada_id)
    participante_pelada_usecase = participante_factory()
    if request.method == 'POST':
        decoded = request.body.decode('utf-8')
        parsed = parse_qs(decoded)
        num_players = max(len(v) for v in parsed.values())
        players = []
        for i in range(num_players):
            player = {}
            for key, values in parsed.items():
                player[key] = values[i] if i < len(values) else None
            players.append(player)
        for player in players:
            player_dto = ParticipantePelada(
                pelada=pelada,
                usuario=request.user,
                nome=player['player_name'],
                ataque=player['player_attack'],
                velocidade=player['player_speed'],
                defesa=player['player_defense'],
                passe=player['player_pass'],
                controle=player['player_control'],
            )
            response = participante_pelada_usecase.participante_pelada_repository.create_or_update_participante(player_dto)
        return redirect('gerenciador')

    return render(request, 'pelada/editar_pelada.html', {'pelada': pelada_id})


@login_required
def excluir_pelada(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id, criador=request.user)
    if request.method == 'POST':
        pelada.delete()
        return redirect('gerenciador')


@login_required
def remove_jogador(request, participante_id):
    participante_pelada_usecase = participante_factory()
    if request.method == 'POST':
        participante = participante_pelada_usecase.participante_pelada_repository.delete_participante(participante_id)
        return redirect('gerenciador')