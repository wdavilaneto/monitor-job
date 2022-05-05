from pprint import pprint

from trello import Board, Card
import logging.config

from app.default_importer import DefaultImporter
from config import config

ID_POLICIAL_READY = '5f0dd7789edaca5954e380e0'
ID_POLICIAL_DONE = '5ef40250af1aa575945442e6'


class PolicialImporter(DefaultImporter):

    def get_done_list(self, board: Board):
        if board.id == ID_POLICIAL_READY:
            end_workflow = board.get_list('5f0dd7789edaca5954e380e8')
        if board.id == ID_POLICIAL_DONE:
            end_workflow = board.get_list('5ef40250af1aa575945442f4')
        logging.info("Workflow ends on: " + end_workflow.name)
        return end_workflow

    # def get_start(self, card: Card, movimentos=None):
    #     """ Get the beginig of the contabilization or Initial DEvelopint Process for Cycle Time """
    #     if movimentos and len(movimentos):
    #         for movement in movimentos:
    #             pprint(movement)
    #             if movimentos['source']['id'] = '5f0dd7789edaca5954e380e5'
    #         first_mov = movimentos[-1]['datetime']
    #     else:
    #         first_mov = card.created_date
    #     return first_mov

    def execute(self, board: Board, upsert_callback):
        logging.info("Processando Policial: " + board.name)
        if board.id == ID_POLICIAL_READY or board.id == ID_POLICIAL_DONE:
            return super(PolicialImporter, self).execute(board, upsert_callback)
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
    board = ts.get_board(ID_POLICIAL_DONE)
    for l in board.list_lists():
        print((l.name, l.id))
    im = PolicialImporter()
    result = im.execute(board, callback_placeholder)
    print("processou: " + str(result))
    print("done list: ", im.get_done_list(board).name)
