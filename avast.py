#!/Users/cmass/.virtualenv/scrabble-django-27/bin/python

import sys
sys.path.append('./engine')

import csv
import threading
from multiprocessing import Queue
from time import time
# from copy import deepcopy

from word_lookup import WordLookup
from config import ScrabbleConfig, Coordinate
from setup import *

wl = WordLookup()

exitFlag = 0

class GameThread (threading.Thread):
    def __init__(self, q, i, ui, j, uj, wl, n):
        threading.Thread.__init__(self)
        self.q = q
        self.i = i
        self.ui = ui
        self.j = j
        self.uj = uj
        self.wl = wl
        self.n = n

    def run(self):
        do_game(self.q, self.i, self.ui, self.j, self.uj, self.wl, self.n)
        


def do_game(q, i, ui, j, uj, wl, n):
    state = setup_game_state(wl, 'com1', 'com2', False)
    apply_setup_values(state, wl, state.players[0], i, ui)
    apply_setup_values(state, wl, state.players[1], j, uj)

    # try:
    start = time()

    outcome = state.continue_game()

    elapsed = time() - start

    q.put([ n, provider_code_mapping(i), provider_code_mapping(j), utility_code_mapping(ui), utility_code_mapping(uj), outcome[0], outcome[1], elapsed ])
    # except Exception as e:
        # print e.args

with open('report.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["match #", "com1 strategy", "com2 strategy", "com1 utility", "com2 utility", "winning strategy", "winning utility", "seconds"])

    for i in range(0,4):
        for j in range(0,4):
            for ui in range(0,5):
                for uj in range(0,5):
                    threads = []
                    q = Queue()

                    for n in range(0, 10):
                        t = GameThread(q, i, ui, j, uj, wl, n)
                        t.start()
                        threads.append(t)

                    for t in threads:
                        t.join()
                        
                    rows = []
                    while not q.empty():
                        rows.append(q.get())
                    rows.sort(key=lambda r: r[0])

                    for r in rows:
                        writer.writerow(r)


csvfile.close()
