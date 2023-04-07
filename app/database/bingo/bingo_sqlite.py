from utils.json_db import json_montado


def insert_db_vazio(db, g) -> None:
    try:
        db.execute(
            'INSERT INTO bolasDoBingo (rankingJson, bolasDoBingoJson, '
            'author_id) VALUES (?, ?, ?)', (str({}), str({}), g.user['id'])
        )
        db.commit()
    except Exception as e:
        print('Erro encontrado em: ', e)
        raise db.IntegrityError


def select_dict(db, g):
    return [dict(row) for row in db.execute(
        # 'SELECT p.id, author_id, bolasDoBingoJson, username'
        # 'SELECT p.id, title, body, created, author_id, username'
        # ' FROM post p JOIN user u ON p.author_id = u.id'
        # ' ORDER BY created DESC'
        f'SELECT p.id, author_id, bolasDoBingoJson, rankingJson, username'
        f' FROM bolasDoBingo p JOIN user u ON p.author_id = {g.user["id"]}'
        f' AND u.id = {g.user["id"]}'
    ).fetchall()]


def update_db(db, g, json_mont: json_montado) -> None:
    db.execute(
        'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
        ' WHERE id = ?',
        (str(json_mont),
         g.user['id'], g.user['id'])
    )
    db.commit()
