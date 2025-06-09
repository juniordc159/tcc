from abc import ABC, abstractmethod
from typing import List
from pelada.models import ParticipantePelada

class ParticipantePeladaInterface(ABC):
    """
    Interface para o repositório de ParticipantePelada.
    """

    @abstractmethod
    def create_or_update_participante(self, participante: ParticipantePelada) -> bool:
        raise NotImplementedError("Este método deve ser implementado.")

    @abstractmethod
    def delete_participante(self, participante_id: int) -> bool:
        raise NotImplementedError("Este método deve ser implementado.")

    @abstractmethod
    def get_participante_by_id(self, participante_id: int) -> ParticipantePelada:
        raise NotImplementedError("Este método deve ser implementado.")

    @abstractmethod
    def get_participantes_by_pelada_id(self, pelada_id: int) -> List[ParticipantePelada]:
        raise NotImplementedError("Este método deve ser implementado.")
    
