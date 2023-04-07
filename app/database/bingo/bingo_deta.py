from deta import Deta
from sqlite3 import IntegrityError
from utils.json_db import json_montado


def insert_db_vazio(db, g) -> None:
    db_bolas = db.Base('bolasDoBingo')
    teste_login = _login_id(db_bolas, g.user['id'])
    try:
        if (0 if teste_login is None else len(teste_login)) > 0:
            raise IntegrityError
        db_bolas.insert(
            {'rankingJson': str({}),
             'bolasDoBingoJson': str({}),
             'author_id': g.user['id'],
             'id': g.user['id']}
        )
    except IntegrityError:
        pass
    except Exception as e:
        print('Erro encontrado em: ', e)
        raise IntegrityError


def _login_id(db: Deta.Base, user_id):
    items = db.fetch({"id": user_id}).items
    if len(items) == 0:
        return None
    return items[0]


def select_dict(db, g):
    dados = db.Base('bolasDoBingo')
    username = db.Base('user').fetch({"id": g.user["id"]}).items[0]['username']
    dados = dados.fetch({"author_id": g.user["id"]}).items[0]
    dados['username'] = username
    return [dados]


def update_db(db, g, json_mont: json_montado) -> None:
    dados = db.Base('bolasDoBingo')
    key = dados.fetch({"id": g.user["id"]}).items[0]['key']
    dados.update({'bolasDoBingoJson': str(json_mont)}, key=key)
