from typing import List
from pelada.interface.participante_pelada_interface import ParticipantePeladaInterface
from pelada.models import ParticipantePelada

class ParticipantePeladaRepository(ParticipantePeladaInterface):

    def create_or_update_participante(request, participante: ParticipantePelada) -> bool:
        try:
            participante.id = None
            participante.save()
            return True
        except ParticipantePelada.DoesNotExist:
            raise Exception("Pelada não encontrada.")
        except Exception as e:
            raise Exception(f"Erro ao criar pelada: {e}")

    def delete_participante(request, participante_id: int) -> bool:
        try:
            participante = ParticipantePelada.objects.get(id=participante_id)
            participante.delete()
            return True
        except ParticipantePelada.DoesNotExist:
            raise Exception("Pelada não encontrada.")
        except Exception as e:
            raise Exception(f"Erro ao deletar pelada: {e}")
    
    def get_participante_by_id(request, participante_id: int) -> ParticipantePelada:
        try:
            return ParticipantePelada.objects.get(id=participante_id)
        except ParticipantePelada.DoesNotExist:
            raise Exception("Participante não encontrado.")
        except Exception as e:
            raise Exception(f"Erro ao obter participante: {e}")

    def get_participantes_by_pelada_id(request, pelada_id: int) -> List[ParticipantePelada]:
        try:
            return ParticipantePelada.objects.filter(pelada_id=pelada_id)
        except ParticipantePelada.DoesNotExist:
            raise Exception("Participantes não encontrados.")
        except Exception as e:
            raise Exception(f"Erro ao obter participantes: {e}")
        