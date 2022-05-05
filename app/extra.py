from trello import Board
import logging.config

from app.default_importer import DefaultImporter
from config import config

ID_EXTRAJUDICIAL = '5e3855eded3f7a0152dcc387'


class ExtraImporter(DefaultImporter):

    def get_done_list(self, board):
        end_workflow = board.get_list('5e6ba05d61631a5b7437d86e')
        logging.info("Workflow ends on: " + end_workflow.name)
        return end_workflow

    def execute(self, board: Board, upsert_callback):
        if board.id == ID_EXTRAJUDICIAL:
            logging.info("Processando Extrajudicial")
            return super(ExtraImporter, self).execute(board, upsert_callback)
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
    board = ts.get_board(ID_EXTRAJUDICIAL)
    # for l in board.list_lists():
    #     print((l.name, l.id))
    im = ExtraImporter()
    result = im.execute(board, callback_placeholder)

    print("processou: " + str(result))
