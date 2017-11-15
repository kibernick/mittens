import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('MITTENS_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://mittens_wearer:freemittens@localhost/mittens'


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'
    TESTING = True
    DEBUG = True
    # WTF_CSRF_ENABLED = False  # Allows form testing
    SQLALCHEMY_DATABASE_URI = 'mysql://mittens_wearer:freemittens@localhost/mittens_test'
