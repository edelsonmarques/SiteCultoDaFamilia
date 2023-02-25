import os
from flask import Flask
# from .utils.momentjs import *


def create_app(test_config=None):
    # create and configure the app Flask
    # app = Flask(__name__, instance_relative_config=True)
    app = Flask(__name__, instance_path=os.path.abspath('./instance'))
    # app.jinja_env.globals['momentjs'] = momentjs
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    import db
    db.init_app(app)

    import auth
    app.register_blueprint(auth.bp)

    # from . import blog
    # app.register_blueprint(blog.bp)

    import bingo
    app.register_blueprint(bingo.bp)
    app.add_url_rule('/', endpoint='index')

    return app.run(debug=True, port=5000)


if __name__ == '__main__':
    create_app()

# export FLASK_APP=flaskr
# export FLASK_ENV=development
# flask run -p 8900

# flask --app flaskr init-db
# flask --app flaskr --debug run --port 8900
