from pydantic import BaseModel
from typing import List


class BolasDoBingoJson(BaseModel):
    ConfAPI: List[str]
    ListaGeral: List[str]
    ListaVisitante: List[str]
    ListaMenor: List[str]
    ListaDinamica: List[str]
    ListaNiverCasamento: List[str]
    ListaEnsaio: List[str]
    MesSorteio: List[str]
    ListaMesSorteio: List[str]
    NomeSorteadoAnterior: List[str]
    NomeSorteado: List[str]
    Opcao: List[str]
    Proximo: List[str]
    Ensaio: List[str]
    HabilitarEnsaio: List[str]

    def __len__(self):
        return self.dict().keys().__len__()


class DadosDict(BaseModel):
    id: int
    author_id: int
    bolasDoBingoJson: BolasDoBingoJson
    rankingJson: str
    username: str

    def __len__(self):
        return self.dict().keys().__len__()
