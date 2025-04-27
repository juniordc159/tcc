from typing import List
from fut_app.pelada.interface.pelada_interface import PeladaInterface
from fut_app.pelada.models import Pelada



class PeladaService():
    def __init__(self, pelada_repository: PeladaInterface):
        self.pelada_repository = pelada_repository
        
def criar_ou_editar_pelada(self, pelada: Pelada) -> bool:
    response = self.pelada_repository.create_or_update_pelada(pelada)
    return response

def excluir_pelada(self, pelada_id: int) -> bool:
    response = self.pelada_repository.delete_pelada(pelada_id)
    return response

def listar_peladas(self, pelada_id: int) -> List[Pelada]:
    response = self.pelada_repository.get_all_peladas(pelada_id)
    return response

def obter_por_id(self, pelada: int) -> Pelada:
    response = self.pelada_repository.get_by_id(pelada)
    if not response:
        raise Exception("Pelada não encontrado.")
    return response



