from typing import List
from pelada.interface.participante_pelada_interface import ParticipantePeladaInterface
from pelada.models import ParticipantePelada



class ParticipantePeladaService():
    def __init__(self, participante_pelada_repository: ParticipantePeladaInterface):
        self.participante_pelada_repository = participante_pelada_repository
        
def criar_ou_editar_participante(self, participante: ParticipantePelada) -> bool:
    response = self.participante_pelada_repository.create_or_update_participante(participante)
    return response

def excluir_participante(self, participante_id: int) -> bool:
    response = self.participante_pelada_repository.delete_participante(participante_id)
    return response

    def get_participante_by_id(self, participante_id: int) -> ParticipantePelada:
        response = self.participante_pelada_repository.get_participante_by_id(participante_id)
    return response

    def get_participantes_by_pelada_id(self, pelada_id: int) -> List[ParticipantePelada]:
        response = self.participante_pelada_repository.get_participantes_by_pelada_id(pelada_id)
    return response
