import logging.config
from pprint import pprint
from trello import Board

import config
from app.default_importer import DefaultImporter

ID_INTEGRACAO_BOARD = '5b9975423903482aae3259dd'


class IntegracaoImporter(DefaultImporter):

    def get_done_list(self, board):
        end_workflow = board.get_list('5b997ac4005a4a22e92a4ff2')
        logging.info("Workflow ends on: " + end_workflow.name)
        return end_workflow

    def execute(self, board: Board, upsert_callback):
        if board.id == ID_INTEGRACAO_BOARD:
            logging.info("Processando Integraçao Board Importer")
            return super(IntegracaoImporter, self).execute(board, upsert_callback)
        else:
            return 0


if __name__ == '__main__':
    def callback_placeholder(d):
        print((d['trello_id'],
               str(d['start'].strftime("%d/%m/%Y")),
               str(d['end'].strftime("%d/%m/%Y")),
               d['cycle_time'], d['label'], d['name']
               ))


    config.logger.setLevel(logging.DEBUG)
    from app.trello_service import TrelloService

    ts = TrelloService()
    board = ts.get_board(ID_INTEGRACAO_BOARD)
    for l in board.list_lists():
        print((l.name, l.id))

    im = IntegracaoImporter()
    result = im.execute(board, callback_placeholder)
    
    print("processou: " + str(result))
