from flask import current_app, g
import sqlite3
import click
from deta import Deta


def get_db():
    if 'db' not in g or type(g.db) is Deta:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    try:
        db.execute(
            # 'SELECT p.id, author_id, bolasDoBingoJson, username'
            # 'SELECT p.id, title, body, created, author_id, username'
            # ' FROM post p JOIN user u ON p.author_id = u.id'
            # ' ORDER BY created DESC'
            f'SELECT * FROM user'
        ).fetchall()
    except sqlite3.OperationalError:
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        click.echo('Initialized the database.')
