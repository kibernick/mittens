from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from mittens.logs.views import blueprint as api
from mittens.db import db
from mittens.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    CORS(app, resources={r"*": {"origins": "*"}})  # TODO: restrict this properly

    # Import models and initialize DB.
    SQLAlchemy(app)
    Migrate(app, db)

    # Register blueprints.
    app.register_blueprint(api, url_prefix='/api/v1')

    return app
