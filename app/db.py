from flask import g
from database import db_sqlite, db_deta
from enums.env_deta import deta_db


def get_db():
    if 'db' not in g:
        if deta_db:
            g.db = db_deta.get_db()
        else:
            g.db = db_sqlite.get_db()
    return g.db


def close_db(_=None):
    db = g.pop('db', None)
    if db is not None and type(db) is not db_deta.Deta:
        db.close()


def init_db():
    if deta_db:
        db_deta.init_db()
    else:
        db_sqlite.init_db()


# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)
    with app.app_context():
        init_db()
