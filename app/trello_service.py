import logging
from pprint import pprint
from trello import TrelloClient
from config import config


class TrelloService:

    def __init__(self):
        self.config = config
        self.client = TrelloClient(
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            token=config.TOKEN,
            token_secret=config.TOKEN_SECRET
        )
        logging.info("Trello Service Started - API Key: " + config.API_KEY)

    def list_boards(self):
        logging.info("Listing boards")
        return self.client.list_boards()

    def get_board(self, _id):
        return self.client.get_board(_id)


if __name__ == '__main__':
    config.logger.setLevel(logging.DEBUG)
    ts = TrelloService()
    pprint(ts.list_boards())
