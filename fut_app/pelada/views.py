import json
import io
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary
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
            
            existing_players = {str(p.id): p for p in ParticipantePelada.objects.filter(pelada=pelada)}
            
            for key, value in request.POST.items():
                if key.startswith('player_name_'):
                    player_id = key.split('_')[2]
                    
                    if player_id == 'new':
                        try:
                            nome = value
                            selected = request.POST.get(f'player_selected_{player_id}') == 'on'
                            ataque = min(max(int(request.POST.get(f'player_attack_{player_id}', 3)), 1), 5)
                            defesa = min(max(int(request.POST.get(f'player_defense_{player_id}', 3)), 1), 5)
                            velocidade = min(max(int(request.POST.get(f'player_speed_{player_id}', 3)), 1), 5)
                            controle = min(max(int(request.POST.get(f'player_control_{player_id}', 3)), 1), 5)
                            passe = min(max(int(request.POST.get(f'player_pass_{player_id}', 3)), 1), 5)
                            
                            player = ParticipantePelada.objects.create(
                                pelada=pelada,
                                usuario=pelada.criador,
                                nome=nome,
                                selected=selected,
                                ataque=ataque,
                                defesa=defesa,
                                velocidade=velocidade,
                                controle=controle,
                                passe=passe
                            )
                            existing_players[str(player.id)] = player
                        except Exception as e:
                            messages.error(request, f'Erro ao criar jogador: {str(e)}')
                            continue
                    elif player_id in existing_players:
                        player = existing_players[player_id]
                        try:
                            player.nome = value
                            player.selected = request.POST.get(f'player_selected_{player_id}') == 'on'
                            player.ataque = min(max(int(request.POST.get(f'player_attack_{player_id}', player.ataque)), 1), 5)
                            player.defesa = min(max(int(request.POST.get(f'player_defense_{player_id}', player.defesa)), 1), 5)
                            player.velocidade = min(max(int(request.POST.get(f'player_speed_{player_id}', player.velocidade)), 1), 5)
                            player.controle = min(max(int(request.POST.get(f'player_control_{player_id}', player.controle)), 1), 5)
                            player.passe = min(max(int(request.POST.get(f'player_pass_{player_id}', player.passe)), 1), 5)
                            player.save()
                        except Exception as e:
                            messages.error(request, f'Erro ao atualizar jogador: {str(e)}')
                            continue
            
            for key, value in request.POST.items():
                if key.startswith('player_removed_'):
                    player_id = key.split('_')[2]
                    if player_id in existing_players:
                        try:
                            player = existing_players[player_id]
                            player.delete()
                        except Exception as e:
                            messages.error(request, f'Erro ao remover jogador: {str(e)}')
                            continue
            
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
    
    jogadores = participante_pelada_usecase.participante_pelada_repository.get_participantes_by_pelada_id(pelada_id)
    
    jogadores_selecionados_ids = json.loads(request.POST.get('jogadores_selecionados[]', '[]'))
    
    jogadores_selecionados = [j for j in jogadores if str(j.id) in jogadores_selecionados_ids]
    planilha = formatar_jogadores_para_planilha(jogadores_selecionados)
    if len(jogadores_selecionados) < 12:
        messages.error(request, "É necessário ter pelo menos 12 jogadores selecionados para sortear os times.")
        return redirect('editar_pelada', pelada_id=pelada_id)
    

    
    # Parâmetros
    jogadores = planilha['Jogador'].tolist()
    n_jogadores = len(jogadores)
    n_times = 3
    atributos = ['NotaGeral', 'DEF', 'ATAQUE', 'VEL', 'PASSE', 'CONTROL']

    # Criar o modelo
    modelo = LpProblem("Formacao_de_Times", LpMinimize)

    # Variáveis de decisão
    x = {
        (i, j): LpVariable(f"x_{i}_{j}", cat=LpBinary)
        for i in range(n_jogadores)
        for j in range(n_times)
    }

    # Cada jogador em apenas 1 time
    for i in range(n_jogadores):
        modelo += lpSum(x[i, j] for j in range(n_times)) == 1

    # Controlar a quantidade por time
    base = n_jogadores // n_times
    extra = n_jogadores % n_times

    for j in range(n_times):
        if j < extra:
            modelo += lpSum(x[i, j] for i in range(n_jogadores)) == base + 1
        else:
            modelo += lpSum(x[i, j] for i in range(n_jogadores)) == base

    # ➕ Restrição: Jogador fraco (NotaGeral < 2.0) - no máximo 1 por time
    jogadores_fracos = [i for i in range(n_jogadores) if planilha.loc[i, 'NotaGeral'] < 2.0]
    for j in range(n_times):
        modelo += lpSum(x[i, j] for i in jogadores_fracos) <= 1, f"Max_um_jogador_fraco_time_{j+1}"

    # Soma das notas gerais por time
    nota_time = {
        j: lpSum(x[i, j] * planilha.loc[i, 'NotaGeral'] for i in range(n_jogadores))
        for j in range(n_times)
    }

    # Variáveis auxiliares
    nota_max = LpVariable("nota_max")
    nota_min = LpVariable("nota_min")

    # Restrições de nota máxima/mínima
    for j in range(n_times):
        modelo += nota_time[j] <= nota_max
        modelo += nota_time[j] >= nota_min

    # Objetivo: minimizar a diferença
    modelo += nota_max - nota_min

    # Resolver
    modelo.solve()

    # Organizar jogadores por time
    times = {j+1: [] for j in range(n_times)}
    somas = {j+1: {atrib: 0 for atrib in atributos} for j in range(n_times)}

    for i in range(n_jogadores):
        for j in range(n_times):
            if x[i, j].varValue == 1:
                jogador = planilha.loc[i]
                times[j+1].append(jogador['Jogador'])
                for atrib in atributos:
                    somas[j+1][atrib] += jogador[atrib]

    time1 = []
    time2 = []
    time3 = []
    
    times = atribuir_times_por_nome(jogadores_selecionados, times)
    context = {
        'pelada': pelada,
        'time1': times[1],
        'time2': times[2],
        'time3': times[3],
        'media_time1': float(somas[1]['NotaGeral']),
        'media_time2': float(somas[2]['NotaGeral']),
        'media_time3': float(somas[3]['NotaGeral']),
    }
    
    return render(request, 'pelada/resultado_sorteio.html', context)
# @login_required
# def sortear_times(request, pelada_id):
#     pelada = get_object_or_404(Pelada, id=pelada_id, criador=request.user)
#     participante_pelada_usecase = participante_factory()
    
#     jogadores = participante_pelada_usecase.participante_pelada_repository.get_participantes_by_pelada_id(pelada_id)
    
#     jogadores_selecionados_ids = json.loads(request.POST.get('jogadores_selecionados[]', '[]'))
    
#     jogadores_selecionados = [j for j in jogadores if str(j.id) in jogadores_selecionados_ids]
#     if len(jogadores_selecionados) < 12:
#         messages.error(request, "É necessário ter pelo menos 12 jogadores selecionados para sortear os times.")
#         return redirect('editar_pelada', pelada_id=pelada_id)
    
#     if len(jogadores_selecionados) > 18:
#         messages.error(request, "O número máximo de jogadores selecionados é 18 (6 jogadores por time).")
#         return redirect('editar_pelada', pelada_id=pelada_id)
    
#     for jogador in jogadores_selecionados:
#         jogador.media = (jogador.ataque + jogador.defesa + jogador.velocidade + jogador.controle + jogador.passe) / 5
    
#     jogadores_ordenados = sorted(jogadores_selecionados, key=lambda x: x.media, reverse=True)
    
#     time1 = []
#     time2 = []
#     time3 = []
    
#     for i in range(0, len(jogadores_ordenados), 3):
#         if i < len(jogadores_ordenados) and len(time1) < 6:
#             time1.append(jogadores_ordenados[i])
#         if i + 1 < len(jogadores_ordenados) and len(time2) < 6:
#             time2.append(jogadores_ordenados[i + 1])
#         if i + 2 < len(jogadores_ordenados) and len(time3) < 6:
#             time3.append(jogadores_ordenados[i + 2])
    
#     media_time1 = sum(j.media for j in time1) / len(time1) if time1 else 0
#     media_time2 = sum(j.media for j in time2) / len(time2) if time2 else 0
#     media_time3 = sum(j.media for j in time3) / len(time3) if time3 else 0
    
#     context = {
#         'pelada': pelada,
#         'time1': time1,
#         'time2': time2,
#         'time3': time3,
#         'media_time1': round(media_time1, 1),
#         'media_time2': round(media_time2, 1),
#         'media_time3': round(media_time3, 1),
#     }
    
#     return render(request, 'pelada/resultado_sorteio.html', context)

def formatar_jogadores_para_planilha(jogadores_selecionados):
    if not jogadores_selecionados:
        raise ValueError("A lista de jogadores selecionados está vazia.")

    linhas = []
    for jogador in jogadores_selecionados:
        media = (jogador.ataque + jogador.defesa + jogador.velocidade + jogador.controle + jogador.passe) / 5
        linha = f"{jogador.nome},\"{media:.2f}\",{jogador.defesa},\"{jogador.ataque:.2f}\",\"{jogador.velocidade:.2f}\",\"{jogador.passe:.2f}\",\"{jogador.controle:.2f}\""
        linhas.append(linha)

    conteudo_csv = '\n'.join(linhas)
    planilha = pd.read_csv(io.StringIO(conteudo_csv), header=None)
    planilha.columns = ['Jogador', 'NotaGeral', 'DEF', 'ATAQUE', 'VEL', 'PASSE', 'CONTROL']

    for col in ['NotaGeral', 'DEF', 'ATAQUE', 'VEL', 'PASSE', 'CONTROL']:
        planilha[col] = planilha[col].astype(str).str.replace(",", ".").astype(float)

    return planilha

def atribuir_times_por_nome(jogadores_selecionados, times_por_nome):
    times = {1: [], 2: [], 3: []}

    for time_id, nomes in times_por_nome.items():
        for nome in nomes:
            jogador = next((j for j in jogadores_selecionados if j.nome.strip() == nome.strip()), None)
            if jogador:
                times[time_id].append(jogador)

    return times