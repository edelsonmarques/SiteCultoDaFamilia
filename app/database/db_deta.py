from flask import g
import sqlite3
import click
from deta import Deta
from enums.env_deta import projeto_key


def get_db():
    if 'db' not in g:
        deta = Deta(project_key=projeto_key)
        g.db = deta
    return g.db


def init_db():
    db = get_db()
    try:
        db.Base('user').fetch()
        # print(db.Base('user').fetch().items)
    except sqlite3.OperationalError:
        # with current_app.open_resource('schema.sql') as f:
        #     db.executescript(f.read().decode('utf8'))
        click.echo('Initialized the database.')
