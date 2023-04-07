from werkzeug.security import generate_password_hash


def insert_user(db, username, password):
    try:
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        raise db.IntegrityError


def login_user(db, username):
    return db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()


def login_id(db, user_id):
    return db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
