#!/Users/cmass/.virtualenv/scrabble-django-27/bin/python

import sys
sys.path.append('./engine')
from word_lookup import WordLookup
from config import ScrabbleConfig, Coordinate
from setup import *
wl = WordLookup()
setup_game_state(wl, 'asd', 'qwe')
for player in Game.instance.players:
    apply_setup_values(wl, player, 0, 0)

Game.instance.continue_game()
