import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get("MITTENS_SECRET", "secret-key")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP = False
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"
    DEBUG = False
    SQLALCHEMY_USER = "mittens_wearer"
    SQLALCHEMY_PASS = "freemittens"  # :')
    SQLALCHEMY_HOST = "10.0.2.2"
    SQLALCHEMY_DB = "mittens"
    SQLALCHEMY_DATABASE_URI = "mysql://{user}:{pwd}@{host}/{db}".format(
        user=SQLALCHEMY_USER, pwd=SQLALCHEMY_PASS, host=SQLALCHEMY_HOST, db=SQLALCHEMY_DB
    )


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True
    SQLALCHEMY_USER = "mittens_wearer"
    SQLALCHEMY_PASS = "freemittens"
    SQLALCHEMY_HOST = "localhost"
    SQLALCHEMY_DB = "mittens"
    SQLALCHEMY_DATABASE_URI = "mysql://{user}:{pwd}@{host}/{db}".format(
        user=SQLALCHEMY_USER, pwd=SQLALCHEMY_PASS, host=SQLALCHEMY_HOST, db=SQLALCHEMY_DB
    )


class TestConfig(Config):
    """Test configuration."""

    ENV = "test"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_USER = "mittens_wearer"
    SQLALCHEMY_PASS = "freemittens"
    SQLALCHEMY_HOST = "localhost"
    SQLALCHEMY_DB = "mittens_test"
    SQLALCHEMY_DATABASE_URI = "mysql://{user}:{pwd}@{host}/{db}".format(
        user=SQLALCHEMY_USER, pwd=SQLALCHEMY_PASS, host=SQLALCHEMY_HOST, db=SQLALCHEMY_DB
    )
