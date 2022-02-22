import os
from flask import Flask
from enum import Enum

from app.models import db
from config import DevelopmentConfig, ProductionConfig


class Currency(Enum):
    EUR = 978
    USD = 840
    RUB = 643


def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    init_db(app)
    configure_logging(app)
    return app


def configure_logging(app):
    import logging
    from flask.logging import default_handler
    from logging.handlers import RotatingFileHandler
    app.logger.removeHandler(default_handler)
    file_path = os.path.join(os.path.dirname(app.instance_path), 'logs', 'app.log')
    file_handler = RotatingFileHandler(file_path, maxBytes=16384, backupCount=20)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt=u'%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%M-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


app = create_app(ProductionConfig)


from app import views, models, forms
