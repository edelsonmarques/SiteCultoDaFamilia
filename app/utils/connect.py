import requests
import json
import pandas as pd
from db import get_db
from .resources import file_local
from .db_serialize import armazenar_enums, get_dados_dict, DadosDict, List
from .json_db import json_montado


def carregar_api(url: str = '', path_file: str = '') -> json:
    try:
        # url = bolas[0]['bolasDoBingoJson']['ConfAPI'][0]
        # url = ['']
        connect = requests.get(url + '.json')
        connect = connect.json()
    except Exception as e:
        print('Falha na conexão com a API. Erro: ', e)
        connect = file_local(path_file)
    return connect


def carregar_chaves_api(url: str = '', path_file: str = '') -> list:
    connect = carregar_api(url, path_file)
    try:
        chaves = pd.DataFrame(connect['presenca']).keys().values
    except KeyError:
        chaves = ['']
    lista_chaves = [chave for chave in chaves]
    return lista_chaves


def insert_db_vazio(g) -> None:
    db = get_db()
    db.execute(
            'INSERT INTO bolasDoBingo (rankingJson, bolasDoBingoJson, '
            'author_id) VALUES (?, ?, ?)', (str({}), str({}), g.user['id'])
        )
    db.commit()


def update_db(g, json_mont: json_montado) -> None:
    db = get_db()
    db.execute(
        'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
        ' WHERE id = ?',
        (str(json_mont),
         g.user['id'], g.user['id'])
    )
    db.commit()


def select_dict(g) -> List[DadosDict]:
    db = get_db()
    dados = [dict(row) for row in db.execute(
        # 'SELECT p.id, author_id, bolasDoBingoJson, username'
        # 'SELECT p.id, title, body, created, author_id, username'
        # ' FROM post p JOIN user u ON p.author_id = u.id'
        # ' ORDER BY created DESC'
        f'SELECT p.id, author_id, bolasDoBingoJson, rankingJson, username'
        f' FROM bolasDoBingo p JOIN user u ON p.author_id = {g.user["id"]}'
        f' AND u.id = {g.user["id"]}'
        ).fetchall()]
    armazenar_enums(dados)
    # print('dados_dict antes: ', get_dados_dict().json())
    return get_dados_dict()
    # return dados
