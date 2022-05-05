from trello import Board
import logging.config

from app.default_importer import DefaultImporter
from config import config

ID_DESIGN_UI = '5de6c03adf1cb16e4e4a8971'
ID_DESIGN_SYSTEM = '5fcc58720a882a8ad91f840c'


class UxImporter(DefaultImporter):

    def get_done_list(self, board: Board):
        if board.id == ID_DESIGN_SYSTEM:
            end_workflow = board.get_list('600ee54e0cd57f5ba3d7013b')
            logging.info("Workflow ends on: " + end_workflow.name)
        else:
            end_workflow = board.get_list('5f29d90eb48c0469fc60679b')
            logging.info("Workflow ends on: " + end_workflow.name)
        return end_workflow

    def execute(self, board: Board, upsert_callback):
        if board.id == ID_DESIGN_SYSTEM:
            logging.info("Importer: " + board.name)
            return super(UxImporter, self).execute(board, upsert_callback)
        if board.id == ID_DESIGN_UI:
            logging.info("Importer: " + board.name)
            return super(UxImporter, self).execute(board, upsert_callback)
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
    _board = ts.get_board(ID_DESIGN_UI) #
    for l in _board.list_lists():
        print((l.name, l.id))
    im = UxImporter()
    result = im.execute(_board, callback_placeholder)
    print("processou: " + str(result))
