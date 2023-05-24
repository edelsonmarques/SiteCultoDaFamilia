import requests
import json
import pandas as pd
import os
from database.bingo import bingo_sqlite, bingo_deta
from db import get_db
from .resources import file_local
from .db_serialize import armazenar_enums, get_dados_dict, DadosDict, List
from .json_db import json_montado
from enums.env_deta import deta_db


def carregar_api(url: str = '', path_file: str = '') -> json:
    _print = False
    try:
        # url = bolas[0]['bolasDoBingoJson']['ConfAPI'][0]
        # url = ['']
        connect = requests.get(url + '.json')
        connect = connect.json()
    except Exception as e:
        if _print:
            print('Falha na conexão com a API. Erro: ', e)
        connect = None
        # connect = file_local(path_file)
    return connect


def carregar_chaves_api(url: str = '', path_file: str = '') -> list:
    connect = carregar_api(url, path_file)
    try:
        chaves = pd.DataFrame(connect['presenca']).keys().values
    except (KeyError, TypeError):
        chaves = ['']
    lista_chaves = [chave for chave in chaves]
    return lista_chaves


def insert_db_vazio(g) -> None:
    db = get_db()
    if deta_db:
        bingo_deta.insert_db_vazio(db, g)
    else:
        bingo_sqlite.insert_db_vazio(db, g)


def update_db(g, json_mont: json_montado) -> None:
    db = get_db()
    if deta_db:
        bingo_deta.update_db(db, g, json_mont)
    else:
        bingo_sqlite.update_db(db, g, json_mont)


def select_dict(g) -> List[DadosDict]:
    db = get_db()
    if deta_db:
        dados = bingo_deta.select_dict(db, g)
    else:
        dados = bingo_sqlite.select_dict(db, g)
    armazenar_enums(dados)
    # print('dados_dict antes: ', get_dados_dict().json())
    return get_dados_dict()
    # return dados


def insert_file_disk(data, g, name='report.xlsx') -> None:
    db = get_db()
    if deta_db:
        bingo_deta.insert_file_disk(db, data, g, name)
    # else:
    #     bingo_sqlite.insert_db_vazio(db, g)


def select_file_disk(g, name='report.xlsx'):
    db = get_db()
    if deta_db:
        dados = bingo_deta.select_file_disk(db, g, name)
    else:
        dados = bingo_sqlite.select_dict(db, g)
        pass
    return dados
