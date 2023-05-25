from pydantic import BaseModel
from typing import List, Dict


class BolasDoBingoJson(BaseModel):
    ConfAPI: List[str]
    ListaGeral: List[str]
    ListaVisitante: List[str]
    ListaMenor: List[str]
    ListaDinamica: List[str]
    ListaDinamicaMaePai: List[str]
    SelecaoListaMaePai: Dict
    ListaDinamicaFilhosPais: Dict
    SelecaoListaFilhosPais: Dict
    SelecaoEventoEspecial: List[Dict]
    ListaNiverCasamento: List[str]
    ListaEnsaio: List[str]
    ListaEnsaioAlameda: List[str]
    ListaEnsaioJardimCopa1: List[str]
    ListaEnsaioJardimCopa2: List[str]
    ListaEnsaioNovaDivineia1: List[str]
    ListaEnsaioNovaDivineia2: List[str]
    ListaEnsaioPiedade: List[str]
    ListaEnsaioVeneza4: List[str]
    HabilitarListaAlameda: List[str]
    HabilitarListaJardimCopa1: List[str]
    HabilitarListaJardimCopa2: List[str]
    HabilitarListaNovaDivineia1: List[str]
    HabilitarListaNovaDivineia2: List[str]
    HabilitarListaPiedade: List[str]
    HabilitarListaVeneza4: List[str]
    MesSorteio: List[str]
    ListaMesSorteio: List[str]
    NomeSorteadoAnterior: List[str]
    NomeSorteado: List[str]
    HistoricoSorteio: Dict
    Ensaio: List[str]
    HabilitarEnsaio: List[str]
    HabilitarFilhosParaPais: List[str]

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
