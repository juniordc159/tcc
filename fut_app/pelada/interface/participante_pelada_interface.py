from abc import ABC, abstractmethod

class ParticipantePeladaInterface(ABC):
    """
    Interface for ParticipantePelada models.
    """

    @abstractmethod
    def create_or_update_participante(self, data):
        raise NotImplementedError("Este método deve ser substituído.")

    @abstractmethod
    def get_participantes_by_pelada_id(request, pelada_id):
        raise NotImplementedError("Este método deve ser substituído.")

    @abstractmethod
    def get_participante_by_id(request, pelada_id: int):
        raise NotImplementedError("Este método deve ser substituído.")

    @abstractmethod
    def delete_participante(self, pelada_id):
        raise NotImplementedError("Este método deve ser substituído.")
    
