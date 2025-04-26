from .models import Pelada, ParticipantePelada
from django.contrib.auth.models import User

def criar_pelada(criador, dia, hora, local):
    pelada = Pelada.objects.create(
        criador=criador,
        dia=dia,
        hora=hora,
        local=local
    )
    return pelada

def adicionar_jogador(pelada, usuario):
    participante, created = ParticipantePelada.objects.get_or_create(
        pelada=pelada,
        usuario=usuario
    )
    return participante

def atribuir_notas(participante, ataque, velocidade, defesa, passe):
    participante.ataque = ataque
    participante.velocidade = velocidade
    participante.defesa = defesa
    participante.passe = passe
    participante.save()
    return participante
