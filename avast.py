#!/Users/cmass/.virtualenv/scrabble-django-27/bin/python

import sys
sys.path.append('./engine')

import csv

from word_lookup import WordLookup
from config import ScrabbleConfig, Coordinate
from setup import *

wl = WordLookup()

with open('report.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["match #", "com1 strategy", "com2 strategy", "com1 utility", "com2 utility", "winning strategy", "winning utility"])

    for i in range(0,4):
        for j in range(0,4):
            for ui in range(0,5):
                for uj in range(0,5):
                    for n in range(0, 10):
                        print "n: %i" % n
                        setup_game_state(wl, 'com1', 'com2', False)
                        print "com1: %i %i" % (i, ui)
                        print "com1: %i %i" % (j, uj)
                        apply_setup_values(wl, Game.instance.players[0], i, ui)
                        apply_setup_values(wl, Game.instance.players[1], j, uj)

                        try:
                            outcome = Game.instance.continue_game()
                            writer.writerow(n, provider_code_mapping(i), provider_code_mapping(j), utility_code_mapping(ui), utility_code_mapping(uj), outcome[0], outcome[1])                            
                        except Exception as e:
                            print e.args

csvfile.close()
