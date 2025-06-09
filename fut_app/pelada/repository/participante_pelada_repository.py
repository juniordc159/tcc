from typing import List
from pelada.interface.participante_pelada_interface import ParticipantePeladaInterface
from pelada.models import ParticipantePelada

class ParticipantePeladaRepository(ParticipantePeladaInterface):

    def create_or_update_participante(self, participante: ParticipantePelada) -> bool:
        try:
            if participante.id:
                # Atualizar participante existente
                ParticipantePelada.objects.filter(id=participante.id).update(
                    nome=participante.nome,
                    ataque=participante.ataque,
                    velocidade=participante.velocidade,
                    defesa=participante.defesa,
                    passe=participante.passe,
                    controle=participante.controle
                )
            else:
                # Criar novo participante
                participante.save()
            return True
        except ParticipantePelada.DoesNotExist:
            raise Exception("Participante não encontrado.")
        except Exception as e:
            raise Exception(f"Erro ao criar/atualizar participante: {e}")

    def delete_participante(self, participante_id: int) -> bool:
        try:
            participante = ParticipantePelada.objects.get(id=participante_id)
            participante.delete()
            return True
        except ParticipantePelada.DoesNotExist:
            raise Exception("Participante não encontrado.")
        except Exception as e:
            raise Exception(f"Erro ao deletar participante: {e}")
    
    def get_participante_by_id(self, participante_id: int) -> ParticipantePelada:
        try:
            return ParticipantePelada.objects.get(id=participante_id)
        except ParticipantePelada.DoesNotExist:
            raise Exception("Participante não encontrado.")
        except Exception as e:
            raise Exception(f"Erro ao obter participante: {e}")

    def get_participantes_by_pelada_id(self, pelada_id: int) -> List[ParticipantePelada]:
        try:
            return list(ParticipantePelada.objects.filter(pelada_id=pelada_id))
        except Exception as e:
            raise Exception(f"Erro ao obter participantes: {e}")
        