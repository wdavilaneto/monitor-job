from trello import Board
import logging.config

from app.default_importer import DefaultImporter
from config import config

ID_JUDICIAL = '5d41e061295f5a0e31734864'
ID_PJE = '5f21de96bffb4304ca7dfb2d'


class JudicialImporter(DefaultImporter):

    def get_done_list(self, board: Board):
        end_workflow = super(JudicialImporter, self).get_done_list(board)
        logging.info("Workflow ends on: " + end_workflow.name)
        if board.id == ID_JUDICIAL:
            end_workflow = board.get_list('5d4354a11ae1aa6affc822f0')
        else:
            end_workflow = board.get_list('5f21e3b5f65984515bf91d36')
        logging.info("Workflow ends on: " + end_workflow.name)
        return end_workflow

    def execute(self, board: Board, upsert_callback):
        if board.id == ID_JUDICIAL:
            logging.info("Processando Judicial ( Judicial Importer ) " + board.name)
            return super(JudicialImporter, self).execute(board, upsert_callback)
        if board.id == ID_PJE:
            logging.info("Processando Judicial PJE ( Judicial Importer ) " + board.name)
            return super(JudicialImporter, self).execute(board, upsert_callback)
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

    _ts = TrelloService()
    _board = _ts.get_board(ID_PJE)
    # for l in _board.list_lists():
    #     print((l.name, l.id))
    im = JudicialImporter()
    result = im.execute(_board, callback_placeholder)
    # print("processou: " + str(result))
