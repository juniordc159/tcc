import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from urllib.parse import parse_qs
from dataclasses import dataclass

from pelada.models import ParticipantePelada, Pelada
from pelada.repository.pelada_repository import PeladaRepository
from pelada.service.pelada_service import PeladaService
from pelada.repository.participante_pelada_repository import ParticipantePeladaRepository
from pelada.service.participante_pelada_service import ParticipantePeladaService

@dataclass
class ParticipantePeladaDTO:
    pelada: Pelada
    usuario: str
    nome: str
    ataque: int
    velocidade: int
    defesa: int
    passe: int
    controle: int

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
    players_dict = [player.to_dict() for player in players]

    return render(request, 'pelada/editar_pelada.html', {'pelada': pelada, 'players': players_dict})

@login_required
def salva_pelada(request, pelada_id):
    if request.method == 'POST':
        try:
            pelada = get_object_or_404(Pelada, id=pelada_id, criador=request.user)
            
            # Obtém todos os jogadores existentes
            existing_players = {str(p.id): p for p in ParticipantePelada.objects.filter(pelada=pelada)}
            
            # Processa os dados do formulário
            for key, value in request.POST.items():
                if key.startswith('player_'):
                    parts = key.split('_')
                    if len(parts) >= 3:
                        field = parts[1]
                        player_id = parts[2]
                        
                        if player_id.startswith('new_'):
                            # Cria um novo jogador
                            if field == 'name':
                                player = ParticipantePelada.objects.create(
                                    pelada=pelada,
                                    nome=value,
                                    selected=request.POST.get(f'player_selected_{player_id}') == 'on',
                                    ataque=int(request.POST.get(f'player_attack_{player_id}', 5)),
                                    defesa=int(request.POST.get(f'player_defense_{player_id}', 5)),
                                    velocidade=int(request.POST.get(f'player_speed_{player_id}', 5)),
                                    controle=int(request.POST.get(f'player_control_{player_id}', 5)),
                                    passe=int(request.POST.get(f'player_pass_{player_id}', 5))
                                )
                                existing_players[player_id] = player
                        elif player_id in existing_players:
                            player = existing_players[player_id]
                            # Atualiza todos os campos de uma vez
                            player.nome = request.POST.get(f'player_name_{player_id}', player.nome)
                            player.selected = request.POST.get(f'player_selected_{player_id}') == 'on'
                            player.ataque = int(request.POST.get(f'player_attack_{player_id}', player.ataque))
                            player.defesa = int(request.POST.get(f'player_defense_{player_id}', player.defesa))
                            player.velocidade = int(request.POST.get(f'player_speed_{player_id}', player.velocidade))
                            player.controle = int(request.POST.get(f'player_control_{player_id}', player.controle))
                            player.passe = int(request.POST.get(f'player_pass_{player_id}', player.passe))
                            player.save()
            
            # Processa jogadores removidos
            for key, value in request.POST.items():
                if key.startswith('player_removed_'):
                    player_id = key.split('_')[2]
                    if player_id in existing_players:
                        existing_players[player_id].delete()
            
            messages.success(request, 'Alterações salvas com sucesso!')
            return redirect('editar_pelada', pelada_id=pelada.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao salvar a pelada: {str(e)}')
            return redirect('editar_pelada', pelada_id=pelada_id)
    
    return redirect('gerenciador')


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

@login_required
def sortear_times(request, pelada_id):
    pelada = get_object_or_404(Pelada, id=pelada_id, criador=request.user)
    participante_pelada_usecase = participante_factory()
    
    # Obter todos os jogadores da pelada
    jogadores = participante_pelada_usecase.participante_pelada_repository.get_participantes_by_pelada_id(pelada_id)
    
    # Obter IDs dos jogadores selecionados do POST
    jogadores_selecionados_ids = json.loads(request.POST.get('jogadores_selecionados[]', '[]'))
    
    # Filtrar apenas os jogadores selecionados
    jogadores_selecionados = [j for j in jogadores if str(j.id) in jogadores_selecionados_ids]
    
    # Verificar se há pelo menos 12 jogadores selecionados
    if len(jogadores_selecionados) < 12:
        messages.error(request, "É necessário ter pelo menos 12 jogadores selecionados para sortear os times.")
        return redirect('editar_pelada', pelada_id=pelada_id)
    
    # Verificar se há mais de 18 jogadores selecionados
    if len(jogadores_selecionados) > 18:
        messages.error(request, "O número máximo de jogadores selecionados é 18 (6 jogadores por time).")
        return redirect('editar_pelada', pelada_id=pelada_id)
    
    # Calcular médias dos jogadores
    for jogador in jogadores_selecionados:
        jogador.media = (jogador.ataque + jogador.defesa + jogador.velocidade + jogador.controle + jogador.passe) / 5
    
    # Ordenar jogadores por média
    jogadores_ordenados = sorted(jogadores_selecionados, key=lambda x: x.media, reverse=True)
    
    # Distribuir jogadores em times (máximo 6 por time)
    time1 = []
    time2 = []
    time3 = []
    
    # Distribuir os melhores jogadores alternadamente
    for i in range(0, len(jogadores_ordenados), 3):
        if i < len(jogadores_ordenados) and len(time1) < 6:
            time1.append(jogadores_ordenados[i])
        if i + 1 < len(jogadores_ordenados) and len(time2) < 6:
            time2.append(jogadores_ordenados[i + 1])
        if i + 2 < len(jogadores_ordenados) and len(time3) < 6:
            time3.append(jogadores_ordenados[i + 2])
    
    # Calcular médias dos times
    media_time1 = sum(j.media for j in time1) / len(time1) if time1 else 0
    media_time2 = sum(j.media for j in time2) / len(time2) if time2 else 0
    media_time3 = sum(j.media for j in time3) / len(time3) if time3 else 0
    
    context = {
        'pelada': pelada,
        'time1': time1,
        'time2': time2,
        'time3': time3,
        'media_time1': round(media_time1, 1),
        'media_time2': round(media_time2, 1),
        'media_time3': round(media_time3, 1),
    }
    
    return render(request, 'pelada/resultado_sorteio.html', context)