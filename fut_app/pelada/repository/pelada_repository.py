from typing import List
from pelada.interface.pelada_interface import PeladaInterface
from pelada.models.pelada import Pelada

class PeladaRepository(PeladaInterface):

    def get_all_peladas(request) -> List[Pelada]:
        return Pelada.objects.all()

    def get_pelada_by_id(request, pelada_id: int) -> Pelada:
        return Pelada.objects.get(id=pelada_id)

    def create_or_update_pelada(request, pelada: Pelada) -> Pelada:
        try:
            pelada.save()
            return True
        except Exception as e:
            raise Exception(f"Erro ao criar pelada: {e}")

    def delete_pelada(request, pelada_id: int) -> bool:
        try:
            pelada = Pelada.objects.get(id=pelada_id)
            pelada.delete()
            return True
        except Pelada.DoesNotExist:
            raise Exception("Pelada não encontrada.")
        except Exception as e:
            raise Exception(f"Erro ao deletar pelada: {e}")