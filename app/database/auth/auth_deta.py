from werkzeug.security import generate_password_hash
from deta import Deta
from sqlite3 import IntegrityError


def insert_user(db: Deta.Base, username, password):
    db_user = db.Base('user')
    tamanho = len(db_user.fetch().items)
    try:
        teste_login = login_user(db, username)
        if (0 if teste_login is None else len(teste_login)) > 0:
            raise IntegrityError
        db_user.insert(
            {'username': username,
             'password': generate_password_hash(password),
             "id": tamanho+1}
        )
    except IntegrityError:
        raise IntegrityError


def login_user(db: Deta.Base, username):
    items = db.Base('user').fetch({"username": username}).items
    if len(items) == 0:
        return None
    return items[0]


def login_id(db: Deta.Base, user_id):
    items = db.Base('user').fetch({"id": user_id}).items
    if len(items) == 0:
        return None
    return items[0]
