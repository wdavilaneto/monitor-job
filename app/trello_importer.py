import logging
from pprint import pprint

from app.default_importer import DefaultImporter
from app.extra import ExtraImporter
from app.integracao import IntegracaoImporter
from app.judicial import JudicialImporter
from app.policial import PolicialImporter
from app.trello_service import TrelloService
from app.ux import UxImporter
from config import config


class TrelloImporter:

    def __init__(self):
        self.config = config
        self.client = TrelloService()
        self.importers = [JudicialImporter()]
        # self.importers = [PolicialImporter(), JudicialImporter(), ExtraImporter(), IntegracaoImporter(), UxImporter(),
        #                   DefaultImporter(), ]
        logging.info("Registered Importers: " + str(self.importers))

    def task_import(self, _id, callback_persist):
        board = self.client.get_board(_id)

        for command in self.importers:
            total_processed = command.execute(board, callback_persist)
            if total_processed:
                break


if __name__ == "__main__":
    # config.logger.setLevel()
    ts = TrelloService()
    # policial = ts.get_board('605a13263b86693cd665d594')
    # portfolio = ts.get_board('605a13263b86693cd665d594')
    # for each in portfolio.list_lists():
    #     pprint(each.id + " " + each.name)
    for each in ts.list_boards():
        pprint(each.id + " " + each.name)
