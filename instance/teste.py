import json
import pandas as pd
from datetime import datetime, date

def pegarMes():
    mesAtual = date.today().month
    if mesAtual in [1, 'fevereiro']:
        mesAtual = 'janeiro'
    elif mesAtual in [2]:
        mesAtual = 'fevereiro'
    elif mesAtual in [11]:
        mesAtual = 'novembro'
    elif mesAtual in [12]:
        mesAtual = 'dezembro'
    elif mesAtual in [3]:
        mesAtual = 'março'
    elif mesAtual in [4]:
        mesAtual = 'abril'
    elif mesAtual in [5]:
        mesAtual = 'maio'
    elif mesAtual in [6]:
        mesAtual = 'junho'
    elif mesAtual in [7]:
        mesAtual = 'julho'
    elif mesAtual in [8]:
        mesAtual = 'agosto'
    elif mesAtual in [9]:
        mesAtual = 'setembro'
    else:
        mesAtual = 'outubro'
    return mesAtual


##################  Não copiar, pois já vai pegar o mês correto  #########################
# mes = 'janeiro'
mes = pegarMes()
with open('E:\\WebOS_CLI\\APPS\\bingoApp\\python\\instance\\teste.json', encoding='utf-8') as file:
    conect = json.load(file)
# dados = pd.DataFrame(conect.json())
dados = pd.DataFrame(conect['presenca'][mes])

##################  Não copiar, pois já vai pegar o mês correto  #########################


def juntar(df, coluna):
    df[coluna] = df[coluna].apply(str)
    return df


def retornarIdade(nascimento):
    if nascimento != 'nan':
        nascimento = datetime.strptime(nascimento, "%d/%m/%Y").date()
        today = date.today()
        return str(today.year - nascimento.year - ((today.month,
                                          today.day) < (nascimento.month,
                                                        nascimento.day)))
    else:
        return nascimento


def niverCasamento(casamento):
    if casamento not in ['nan', '']:
        casamento = datetime.strptime(casamento, "%d/%m/%Y").date()
        casamento = casamento.month
        if casamento in [1, 2]:
            casamento = 2
        elif casamento in [11, 12]:
            casamento = 11
        if mes.lower() in ['janeiro', 'fevereiro']:
            mesTeste = 2
        elif mes.lower() in ['novembro', 'dezembro']:
            mesTeste = 11
        elif mes.lower() in ['março']:
            mesTeste = 3
        elif mes.lower() in ['abril']:
            mesTeste = 4
        elif mes.lower() in ['maio']:
            mesTeste = 5
        elif mes.lower() in ['junho']:
            mesTeste = 6
        elif mes.lower() in ['julho']:
            mesTeste = 7
        elif mes.lower() in ['agosto']:
            mesTeste = 8
        elif mes.lower() in ['setembro']:
            mesTeste = 9
        else:
            mesTeste = 10
        if casamento == mesTeste:
            return True
        else:
            return False
    else:
        return False


dados = dados.transpose()
for column in dados:
    dados = juntar(dados, column)
dados['numCartao'] = dados['idNumero'].apply(lambda x: x.split('/')[1])
dados['congregacao'] = dados['idNumero'].apply(lambda x: x.split('/')[0])
dados['juntosConjuge'] = (dados['nomeConjuge'] + '|' +
                          dados['congregacao'] + '|' +
                          dados['numCartao'] + '|' +
                          dados['nascimentoConjuge'].apply(retornarIdade) + '|' +
                          dados['dataCasamento'] + '|' +
                          dados['nomeTitular'])
dados['juntosTitular'] = (dados['nomeTitular'] + '|' +
                          dados['congregacao'] + '|' +
                          dados['numCartao'] + '|' +
                          dados['nascimentoTitular'].apply(retornarIdade) + '|' +
                          dados['dataCasamento'] + '|' +
                          dados['nomeConjuge'])
colunas = ['idNumero', 'nomeTitular', 'nomeConjuge', 'congregacao', 'numCartao', 'nascimentoConjuge', 'nascimentoTitular', 'dataCasamento']
dados = dados.drop(columns=colunas)
print(dados, '\n')
print(dados['juntosConjuge'][0])
print(dados['juntosTitular'][0])
dados = dados.transpose()
listaGeral = list()
listaDinamica = list()
listaVisitante = list()
listaMenor = list()
listaNiverCasamento = list()
listaEnsaio = list()
for column in dados:
    for index in dados[column]:
        index = str(index).removesuffix('nan')
        if str(index) != str(index).removesuffix('nan|'):
            index = str(index).removesuffix('nan|') + '|'
        if str(index) == str(index).removeprefix('nan|'):
            if str(index).split('|')[1].lower() == 'visitante':
                listaVisitante.append(index)
            elif int(str(index).split('|')[3]) < 18:
                listaMenor.append(index)
            else:
                listaGeral.append(index)
                if niverCasamento(str(index).split('|')[4]):
                    listaNiverCasamento.append(index)
print()
# print(conect)
print(f'listaGeral: {listaGeral}')
print(f'listaVisitante: {listaVisitante}')
print(f'listaMenor: {listaMenor}')
print(f'listaDinamica: {listaDinamica}')
print(f'listaNiverCasamento: {listaNiverCasamento}')
print(f'listaEnsaio: {listaEnsaio}')
print()
# for usuario in dados:
#     for nome in dados[usuario]:
#         print(nome)
# print()