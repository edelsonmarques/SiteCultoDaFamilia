import pandas as pd
from enums import mes as meses
from cultoparafamilia.db.firebase import load_lista_presenca
from cultoparafamilia.sorteio_familia.models import Presencas, DadosDict, Caracteristicas, Lista
from utils.dates import niver_casamento


def load_month(dados: DadosDict, mes):
    # Realizar chamada para o banco da API
    limpar_base(dados)
    dados.mesSorteio = mes
    mes = mes.lower()
    # TODO: Fazer insersão do mes de seminário
    presencas = load_lista_presenca()[mes]
    # for cartao in presenca_mensal
    # ConfAPI = bolasDoBingoJson.ConfAPI[0]
    # ConfAPI = carregar_api(ConfAPI)
    # try:
    #     dados = pd.DataFrame(ConfAPI['presenca'][mes[0]])
    # except (KeyError, TypeError):
    #     if mes[0].__contains__(meses.NOVEMBRO):
    #         dados = pd.DataFrame()
    #     else:
    #         return redirect(url_for('bingo.config', _id=_id))
    
    if mes.__contains__(meses.NOVEMBRO):
        pass
    #     usuarios_temp = pd.DataFrame(ConfAPI['usuarios'])
    #     usuarios_temp = usuarios_temp.transpose()
    #     usuarios_temp['cong_temp'] = usuarios_temp['idNumero'].apply(
    #         lambda x: x.split('/')[0])
    #     usuarios_temp = usuarios_temp.loc[
    #         usuarios_temp.cong_temp != congregacoes.SO_VISITANTE].drop(
    #         columns='cong_temp')
    #     dados = dados.transpose()
    #     # print(dados)
    #     # print(usuarios_temp)
    #     dados = pd.concat([dados, usuarios_temp]).drop_duplicates(
    #         subset='idNumero', keep='last')
    #     print(dados.loc[dados.idNumero == 'Nova Divinéia/31'])
    else:
        presenca_mensal = Presencas(presencas)
    
    dados = presenca_mensal.insert_lists(dados, mes)
    return dados
    
def limpar_base(dados: DadosDict):
    dados.reset_mes()
    return dados

# def congregacao_idnumero(self, i):
#     cartao: Caracteristicas = self.root[i]
#     quebra = cartao.idNumero.split('/')
#     cartao.congregacao = quebra[0]
#     cartao.idNumero = quebra[1]
