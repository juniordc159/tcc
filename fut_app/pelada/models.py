from django.db import models
from django.contrib.auth.models import User

class Pelada(models.Model):
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='peladas_criadas')
    dia = models.DateField()
    hora = models.TimeField()
    local = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pelada em {self.local} no dia {self.dia}"

class ParticipantePelada(models.Model):
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE, related_name='participantes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ataque = models.IntegerField(default=0)
    velocidade = models.IntegerField(default=0)
    defesa = models.IntegerField(default=0)
    passe = models.IntegerField(default=0)

    class Meta:
        unique_together = ('pelada', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} na pelada {self.pelada.local} ({self.pelada.dia})"
