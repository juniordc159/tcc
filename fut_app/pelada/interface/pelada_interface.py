from abc import ABC, abstractmethod

class PeladaInterface(ABC):
    """
    Interface for Pelada models.
    """

    @abstractmethod
    def create_or_update_pelada(self, data):
        raise NotImplementedError("Este método deve ser substituído.")

    @abstractmethod
    def get_all_peladas(request):
        raise NotImplementedError("Este método deve ser substituído.")

    @abstractmethod
    def get_pelada_by_id(request, pelada_id: int):
        raise NotImplementedError("Este método deve ser substituído.")

    @abstractmethod
    def delete_pelada(self, pelada_id):
        raise NotImplementedError("Este método deve ser substituído.")
