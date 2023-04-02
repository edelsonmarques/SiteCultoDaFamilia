from .converter import converter_str_json
from classes.db_classes import DadosDict, List

dados_dict: DadosDict


def armazenar_enums(dados) -> None:
    global dados_dict
    dados[0]['bolasDoBingoJson'] = converter_str_json(dados[0]['bolasDoBingoJson'])
    dados_dict = DadosDict(**dados[0])


def get_dados_dict() -> List[DadosDict]:
    return [dados_dict]
