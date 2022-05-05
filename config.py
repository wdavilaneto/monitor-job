import logging

import yaml
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


def log_initialize():
    # with open('./logging.yaml', 'r') as f:
    with open(path.join(basedir, './logging.yaml'), 'r') as f:
        c = yaml.safe_load(f.read())
        logging.config.dictConfig(c)
    return logging.getLogger(__name__)

class Config(object):
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_DATABASE_URI = "postgresql:///wordcount_dev"  # environ['DATABASE_URL']
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_KEY = environ.get('API_KEY')
    API_SECRET = environ.get('API_SECRET')
    TOKEN = environ.get('TOKEN')
    TOKEN_SECRET = environ.get('TOKEN_SECRET')
    LOOP_SECONDS = environ.get('LOOP_SECONDS')

    def __init__(self):
        basedir = path.abspath(path.dirname(__file__))
        logging.info("Iniciando config ENV: " + basedir)
        load_dotenv(path.join(basedir, '.env'))
        self.APPLICATION_ROOT = environ.get('APPLICATION_ROOT')
        self.SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_ECHO = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.API_KEY = environ.get('API_KEY')
        self.API_SECRET = environ.get('API_SECRET')
        self.TOKEN = environ.get('TOKEN')
        self.TOKEN_SECRET = environ.get('TOKEN_SECRET')
        self.LOOP_SECONDS = environ.get('LOOP_SECONDS')
        self.logger = log_initialize()


logger = log_initialize()
config = Config()
