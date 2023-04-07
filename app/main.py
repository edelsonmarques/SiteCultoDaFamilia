import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app Flask
    # app = Flask(__name__, instance_relative_config=True)
    _app = Flask(__name__, instance_path=os.path.abspath('./instance'))
    # app.jinja_env.globals['momentjs'] = momentjs
    _app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(_app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        _app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        _app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(_app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @_app.route('/hello')
    def hello():
        return 'Hello, World!'

    import db
    db.init_app(_app)

    import auth
    _app.register_blueprint(auth.bp)

    # from . import blog
    # app.register_blueprint(blog.bp)

    import bingo
    _app.register_blueprint(bingo.bp)
    _app.add_url_rule('/', endpoint='index')

    return _app


app = create_app()

# export FLASK_APP=app
# export FLASK_ENV=development
# flask run -p 8900

# flask --app app init-db
# flask --app app --debug run --port 8900
