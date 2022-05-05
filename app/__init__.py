import logging
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Board, Task
from app.trello_importer import TrelloService, TrelloImporter
from config import config

logging.basicConfig(format='[%(levelname)s] [%(asctime)s] - %(message)s', level=logging.DEBUG)

Session = sessionmaker()


def show(l):
    for each in l:
        print(each.id, each.name)


class Portfolio:
    def __init__(self, ts):
        PORTFOLIO = '605a13263b86693cd665d594'
        self.board = ts.get_board(PORTFOLIO)
        self.doing_list = self.board.get_list('605a13263b86693cd665d598')
        self.judicial_list = self.board.get_list('60770b3b64a8036c23635b8c')
        self.extra_list = self.board.get_list('60770b5fa952fe71edd35228')
        self.fisico_list = self.board.get_list('605a13263b86693cd665d59b')
        self.outros_list = self.board.get_list('60770b9ba0b0027fcf2d6296')


class Application():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    Session.configure(bind=engine)  # once engine is available

    # ts = TrelloService()
    trello_importer = TrelloImporter()
    session = Session()

    def run(self):
        loop_time = int(config.LOOP_SECONDS)

        """" Main pipeline """
        while (True):
            logging.info("Initializing an new import Pipeline")
            for board in self.list_selected_boards():
                logging.info("Processing Board: " + board.name)
                try:
                    self.trello_importer.task_import(board.sid, self.save)
                except Exception as ex:
                    logging.error(board.sid)
                    logging.error(ex)
                    # raise ex  # Let the pod End ??

            logging.info("sleeping...")
            time.sleep(loop_time)

    def list_selected_boards(self):
        """ List from Local Database Boards Selected to Be imported """
        return self.session.query(Board).order_by(Board.name).all()

    # Callback Method to save retrieved
    def save(self, retrieved_data):
        """ Callback / Runnable funnction to save each Task (better memeory managment) """
        board = self.session.query(Board).filter_by(sid=retrieved_data['board']).first()
        retrieved = self.session.query(Task).filter_by(board_id=board.id, trello_id=int(retrieved_data['trello_id'])).first()
        if not retrieved and board:
            task = Task()
            # task.id = d['id']
            # task.board = d['board']
            task.board_id = board.id
            task.trello_id = retrieved_data['trello_id']
            task.name = retrieved_data['name']
            task.label = retrieved_data['label']
            task.cycle_time = retrieved_data['cycle_time']
            task.lead_time = retrieved_data['lead_time']
            task.created = retrieved_data['created']
            task.start = retrieved_data['start']
            task.end = retrieved_data['end']
            task.friday = retrieved_data['friday']
            task.card_url = retrieved_data['short_url']
            try:
                self.session.add(task)
                self.session.commit()
                logging.debug("saved:")
                logging.debug(task)
            except Exception as ex:
                logging.error(retrieved_data)
                logging.error(task)
                logging.error(ex)
                raise ex  # Let the pod End...
        else:
            logging.debug("task already exists: ..")
            if not retrieved.card_url:
                logging.debug("updating..")
                retrieved.name = retrieved_data['name']
                retrieved.label = retrieved_data['label']
                retrieved.cycle_time = retrieved_data['cycle_time']
                retrieved.lead_time = retrieved_data['lead_time']
                retrieved.created = retrieved_data['created']
                retrieved.start = retrieved_data['start']
                retrieved.end = retrieved_data['end']
                retrieved.friday = retrieved_data['friday']
                retrieved.card_url = retrieved_data['short_url']
                self.session.add(retrieved)
                self.session.commit()

    def sandbox(self):
        logging.info("Initializing an new import Pipeline")
        # portfolio = self.session.query(Board).filter(Board.sid == PORTFOLIO).first()
        # portfolio = Portfolio(self.ts)
        print(self.list_selected_boards())



def create_app():
    return Application()
