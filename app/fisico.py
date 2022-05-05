from trello import Board
import logging.config

from app.default_importer import DefaultImporter
from config import config

ID_INTEGRA_FISICO = '5e8b3a4c7c9f961b3111ccbc'


class FisicoImporter(DefaultImporter):

    def get_done_list(self, board):
        end_workflow = board.get_list('5eed5e1f5963b333cd234223')
        logging.info("Workflow ends on: " + end_workflow.name)
        return end_workflow

    def execute(self, board: Board, upsert_callback):
        if board.id == ID_INTEGRA_FISICO:
            logging.info("Processando Integraçao Board Importer")
            return super(FisicoImporter, self).execute(board, upsert_callback)
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
    board = ts.get_board(ID_INTEGRA_FISICO)
    # for l in board.list_lists():
    #     print((l.name, l.id))
    im = FisicoImporter()
    result = im.execute(board, callback_placeholder)

    print("processou: " + str(result))
