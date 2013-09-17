from support import Move, PlaceMove, Pass, Game, Tile
from word_lookup import WordLookup
from config import Coordinate, Orientation, the_pusher, GameConfig

from random import shuffle
from copy import deepcopy

class HillClimbingMoveGenerator(object):
    def __init__(self, state, lookup, restart_tries =1):
        self.lookup = lookup
        self.restart_tries = restart_tries
        self.restarts = 0
        # self.__class__.__name__ = ("HillClimbingMoveGenerator(%2i)" % self.restart_tries)
        self.state = state


    def possible_starts(self, word, horizontal):
        highest_start = max(0, (7 - len(word) + 1))

        starts = []
        for i in range(highest_start, 8):
            if horizontal:
                starts.append(Coordinate(i, 7))
            else:
                starts.append(Coordinate(7, i))

        return starts

    def calculate_first_move(self, tiles_in_hand, utility_mapper):
        possible_words = self.lookup.find_all_words([tile.letter for tile in tiles_in_hand])
        horizontal = [True, False]

        best_score = 0.0
        best_move = None

        if GameConfig.debug:
            print "calculate_first_move"

        while self.restarts > 0:
            if GameConfig.debug:
                print "restarts to go: %i" % self.restarts
            stop = False
            current_score = 0.0
            current_move = None
            random_possibilities = deepcopy(possible_words)
            shuffle(random_possibilities)

            if not random_possibilities:
                stop = True
                self.restarts -= 1

            for o in horizontal:
                for word in random_possibilities:
                    for start in self.possible_starts(word, o):
                        if not stop:
                            lts = [ ( start.next(o, i), Tile(word.upper()[i]) ) for i in range(0, len(word)) ]
                            move = Move(dict(lts), self.state)
                            score = utility_mapper(tiles_in_hand, move.letters, self.state)
                            if score > current_score:
                                current_score = score
                                current_move = move
                            else:
                                stop = True
                                self.restarts -= 1
                                if current_score > best_score:
                                    best_score = current_score
                                    best_move = current_move

        if best_score > 0.0:
            return PlaceMove(best_move.letters)
        else:
            return Pass()

    def valid_moves(self, c, word, o, board):
        letter = board.get(c).tile.letter

        unchecked_starts = []
        for i in range(0, len(word)):
            if word.upper()[i] == letter:
                if o == Orientation.horizontal:
                    if (c.x - i) >= 0 and (c.x + len(word) - i) <= 14:
                        unchecked_starts.append( Coordinate(c.x - i, c.y) )
                else:
                    if (c.y - i) >= 0 and (c.y + len(word) - i) <= 14:
                        unchecked_starts.append( Coordinate(c.x, c.y - i) )

        vmoves = []

        for start in unchecked_starts:
            coords_letters = []
            for i in range(0, len(word)):
                coord = start.next(o, i)
                if not board.has_tile(coord):
                    coords_letters.append( (coord, Tile(word.upper()[i])) )

            if coords_letters:
                move = Move(dict(coords_letters), self.state)
                if move.is_valid:
                    vmoves.append(move)
                    if GameConfig.debug:
                        the_pusher[GameConfig.debug_channel].trigger('debug', [{'x': c.x, 'y': c.y, 'tile': {'letter': t.letter, 'score': t.score}} for c, t in move.letters.items()])

        return vmoves

    def calculate_best_move(self, tiles_in_hand, board, utility_mapper):
        letters = [deepcopy(tile.letter) for tile in tiles_in_hand]
        orientations = Orientation.values()

        best_score = 0.0
        best_move = None

        if GameConfig.debug:
            print "calculate_best_move"

        while self.restarts > 0:
            if GameConfig.debug:
                print "restarts to go: %i" % self.restarts
            stop = False
            current_score = 0.0
            current_move = None
            random_squares = deepcopy(board.occupied_squares()).items()
            shuffle(random_squares)
            last_square = random_squares[-1]

            for coordinate in random_squares:
                if GameConfig.debug:
                    the_pusher[GameConfig.debug_channel].trigger('clear_debug')
                if not stop:
                    tile = board.get(coordinate[0]).tile
                    possible_words = self.lookup.find_words_using([tile.letter] + letters, 0)
                    if not possible_words:
                        if coordinate[0] == last_square[0]:
                            stop = True
                            self.restarts -= 1
                    else:
                        last_word = possible_words[-1]

                        for o in orientations:
                            if not stop:
                                for word in possible_words:
                                    if not stop:
                                        moves = self.valid_moves(coordinate[0], word, o, board)
                                        if (not moves) and (coordinate[0] == last_square[0]) and (word == last_word) and o:
                                            stop = True
                                            self.restarts -= 1
                                        for move in moves:
                                            if not stop:
                                                score = utility_mapper(tiles_in_hand, move.letters, self.state)
                                                if score > current_score:
                                                    current_score = score
                                                    current_move = move
                                                else:
                                                    stop = True
                                                    self.restarts -= 1
                                                    if current_score > best_score:
                                                        best_score = current_score
                                                        best_move = current_move

        if best_score > 0.0:
            return PlaceMove(best_move.letters)
        else:
            return Pass()

    def think(self, tiles_in_hand, utility_mapper):
        self.restarts = self.restart_tries
        # Game.instance
        board = self.state.playing_board
        if board.occupied_squares():
            return self.calculate_best_move(tiles_in_hand, board, utility_mapper)
        else:
            return self.calculate_first_move(tiles_in_hand, utility_mapper)
