from typing import List, Dict
from pprint import PrettyPrinter
from __future__ import annotations



pp = PrettyPrinter(width=80, compact=True)

class Board():
    player1_hand: List[str] = []
    player2_hand: List[str] = []
    player1_extra: List[str] = []
    player2_extra: List[str] = []
    player1_gy: List[str] = []
    player2_gy: List[str] = []
    player1_deck: List[str] = []
    player2_deck: List[str] = []
    player1_banished: List[str] = []
    player2_banished: List[str] = []
    current_player: str;

    board_field: List[List[str]];


    def __init__(self, current_player="player1", **kwargs):
        self.current_player = current_player
        board_size = kwargs['board_size'] if 'board_size' in kwargs else 5
        board_field = [['' for i in range(0, board_size)] for i in range(0, board_size)]
        self.__dict__.update(kwargs)
            

    def _create_cardID(self):
        ''' creates the card ID with the cardname + _ + number of times that card appears on the whole board
            e.g. only one Blue-Eyes White Dragon at that game -> Blue-Eyes White Dragon_1 '''
        pass 
        


    def _show_field(self):
        pp.pprint(self.board_field)

    #TODO: calculate delta from this board to previous Board so we get time-reversal mechanics