from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from mittens.api import api
from mittens.auth import login_manager
from mittens.db import db
from mittens.logs.views import blueprint as logs
from mittens.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    CORS(app, resources={r"*": {"origins": "*"}})  # TODO: restrict this properly
    login_manager.init_app(app)

    # Import models and initialize DB.
    SQLAlchemy(app)
    Migrate(app, db)

    # Register blueprints.
    app.register_blueprint(logs)
    api.init_app(app)

    return app
