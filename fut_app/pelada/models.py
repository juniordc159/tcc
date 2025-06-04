from django.db import models
from django.contrib.auth.models import User

class Pelada(models.Model):
    nome = models.CharField(max_length=100)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='peladas_criadas')
    descricao = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ParticipantePelada(models.Model):
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE, related_name='participantes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    ataque = models.IntegerField(default=0)
    velocidade = models.IntegerField(default=0)
    defesa = models.IntegerField(default=0)
    passe = models.IntegerField(default=0)
    controle = models.IntegerField(default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'pelada': self.pelada.id,
            'usuario': self.usuario.username,
            'nome': self.nome,
            'ataque': self.ataque,
            'velocidade': self.velocidade,
            'defesa': self.defesa,
            'passe': self.passe,
            'controle': self.controle
        }

