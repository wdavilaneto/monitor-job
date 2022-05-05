import os
import logging.config
import yaml
from app import create_app


def log_initialize():
    with open('./logging.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    return logging.getLogger(__name__)


logger = log_initialize()

app = create_app()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # app.run()
    app.sandbox()
