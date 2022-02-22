from dotenv import dotenv_values

env = dotenv_values('.env')


class Config(object):
    DEBUG = False
    TESTING = False
    API_SECRET_KEY = env.get('API_SECRET_KEY')
    SECRET_KEY = env.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
    PORT = 8000


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite://:memory:'


class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite://:memory:'
    SECRET_KEY = 'Python3'
