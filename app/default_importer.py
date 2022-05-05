from trello import Board, Card
import datetime
import logging.config
import config


class DefaultImporter:

    def __init__(self):
        self.config = config

    def __get_id_semana(self, date_param):
        process_date = date_param
        while process_date.weekday() != 4:
            process_date += datetime.timedelta(1)
        return process_date

    def __get_main_label(self, labels):
        if labels:
            for label in labels:
                if 'histo' in label.name.lower() or 'funcion' in label.name.lower():
                    return 'História'
                if 'erro' in label.name.lower() or 'corre' in label.name.lower():
                    return 'Correção'
                if 'manut' in label.name.lower() or 'ajuste' in label.name.lower():
                    return 'Ajuste'
                if 'oper' in label.name.lower():
                    return 'Operação'
                if 'débito' in label.name.lower() or 'tarefa técnica' in label.name.lower():
                    return 'Débito'
                if 'atendi' in label.name.lower() or 'suporte' in label.name.lower():
                    return 'Atendimento'
        return 'Outros'

    def get_start(self, card: Card, movimentos=None):
        """ Get the beginig of the contabilization or Initial DEvelopint Process for Cycle Time """
        if movimentos and len(movimentos):
            first_mov = movimentos[-1]['datetime']
        else:
            first_mov = card.created_date
        return first_mov

    def get_end(self, card: Card, movimentos):
        """ Get the end of the contabilization or Initial DEvelopint Process for Cycle Time """
        if len(movimentos):
            last_mov = movimentos[0]['datetime']
        else:
            last_mov = card.created_date
        return last_mov

    def create_dict(self, board: Board, card: Card):
        """ Create default Dict with default (aka non calculated) values """
        d = dict()
        d['id'] = 0
        d['board'] = board.id
        d['trello_id'] = card.idShort
        d['created'] = card.created_date
        d['label'] = self.__get_main_label(card.labels)
        d['name'] = card.name
        d['short_url'] = card.short_url
        return d

    def complement_info(self, d: dict, start, end, creation):
        cycle = end - start
        lead = end - creation
        d['start'] = start
        d['end'] = end
        d['cycle_time'] = max(1, cycle.days)
        d['lead_time'] = max(1, lead.days)
        d['friday'] = self.__get_id_semana(end)

        return d

    def get_done_list(self, board):
        """ Main overidable method to deliver done list"""
        end_workflow = board.list_lists()[-1]
        logging.info("Workflow ends on: " + end_workflow.name)
        return end_workflow

    def get_start_list(self, board):
        return board.list_lists()[0]

    def execute(self, board: Board, upsert_callback):
        logging.info("Start Importer " + __name__ + " Processando: " + board.name)
        # Defaul done list is the Last list
        done_list = self.get_done_list(board)
        cards = done_list.list_cards()

        for card in cards:
            # Default contabilization:  After first change card list is the start, util last List
            movimentos = card.list_movements()
            start = self.get_start(card, movimentos)
            end = self.get_end(card, movimentos)

            d = self.create_dict(board, card)
            d = self.complement_info(d, start, end, card.created_date)
            upsert_callback(d)
        return len(cards)


if __name__ == '__main__':
    config.logger.setLevel(logging.DEBUG)
    from app.trello_service import TrelloService

    ts = TrelloService()

    ID_JUDICIAL = '5d41e061295f5a0e31734864'
    ID_PJE = '5f21de96bffb4304ca7dfb2d'


    def callback_placeholder(d):
        print((d['trello_id'],
               str(d['start'].strftime("%d/%m/%Y")),
               str(d['end'].strftime("%d/%m/%Y")),
               d['cycle_time'], d['label'], d['name']
               ))


    _ts = TrelloService()
    _board = _ts.get_board(ID_JUDICIAL)
    logging.info("Board: " + _board.name)
    default_importer = DefaultImporter()
    default_importer.get_done_list(_board)
    # result = im.execute(_board, callback_placeholder)
    # print("processou: " + str(result))
