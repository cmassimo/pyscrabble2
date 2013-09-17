from support import Move, PlaceMove, Pass, Game, Tile, Run
from word_lookup import WordLookup
from config import Coordinate, Orientation, the_pusher, GameConfig

from copy import deepcopy

class MoveGenerator(object):
    def __init__(self, state, word_lookup):
        self.lookup = word_lookup
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
        moves = []

        if GameConfig.debug:
            print "calculate_first_move"

        for o in horizontal:
            for word in possible_words:
                for start in self.possible_starts(word, o):
                    moves.append( Move( dict( [ (start.next(o, i), Tile(word.upper()[i])) for i in xrange(0, len(word)) ] ), self.state ) )

        positive_scores = [move for move in moves if utility_mapper(tiles_in_hand, move.letters, self.state) > 0.0]

        if positive_scores:
            to_be_played = max(positive_scores, key=lambda ps: utility_mapper(tiles_in_hand, ps.letters, self.state))
            if GameConfig.debug:
                print to_be_played
            return PlaceMove(to_be_played.letters)
        else:
            return Pass()

    def valid_moves(self, c, word, o, board):
        square = board.get(c)
        tile = square.tile
        letter = deepcopy(tile.letter)

        # print "-------------------------------------------- word: %s" % word
        # print "valid_moves, tile on board: %s" % letter

        unchecked_starts = []
        for i in range(0, len(word)):
            if word.upper()[i] == letter:
                if o == Orientation.horizontal:
                    if (c.x - i) >= 0 and (c.x + len(word) - i - 1) <= 14:
                        unchecked_starts.append( Coordinate(c.x - i, c.y) )
                else:
                    if (c.y - i) >= 0 and (c.y + len(word) - i - 1) <= 14:
                        unchecked_starts.append( Coordinate(c.x, c.y - i) )

        # XXX parallel moves WIP

        # ns = c.oriented_neighbors((o + 1) % 2)
        # for i in range(0, len(word)):
        #     for n in ns:
        #         if not board.has_tile(n):
        #             lts = sorted([(c, tile), (n, Tile(word.upper()[i]))], key=lambda x: x[0])
        #             if Run(c, o, dict(lts)).is_valid():
        #                 # if orient:
        #                 #     nc = Coordinate(c.x, c.y - (c.y-n.y))
        #                 #     if nc.is_valid() and (c.x - i) >= 0 and (c.x + len(word) - i) <= 14:
        #                 #         unchecked_starts.append(nc)
        #                 # else:
        #                 #     nc = Coordinate(c.x - (c.x-n.x), c.y)
        #                 #     if nc.is_valid() and (c.y - i) >= 0 and (c.y + len(word) - i) <= 14:
        #                 #         unchecked_starts.append(nc)
        #                 if o == Orientation.horizontal:
        #                     if (c.x - i) >= 0 and (c.x + len(word) - i) <= 14:
        #                         unchecked_starts.append( Coordinate(c.x - i, c.y) )
        #                 else:
        #                     if (c.y - i) >= 0 and (c.y + len(word) - i) <= 14:
        #                         unchecked_starts.append( Coordinate(c.x, c.y - i) )

        # end WIP

        vmoves = []
        for start in unchecked_starts:
            coords_letters = []
            for i in range(0, len(word)):
                coord = start.next(o, i)
                if not board.has_tile(coord):
                    coords_letters.append( (coord, Tile(word.upper()[i])) )
                # else:
                    # print "skipped: %s" % word.upper()[i]
                    

            if coords_letters:
                move = Move(dict(coords_letters), self.state)
                if move.is_valid:
                    vmoves.append(move)
                else:
                    if GameConfig.debug:
                        the_pusher[GameConfig.debug_channel].trigger('debug', [{'x': c.x, 'y': c.y, 'tile': {'letter': t.letter, 'score': t.score}} for c, t in move.letters.items()])

        return vmoves

    def calculate_best_move(self, tiles_in_hand, board, utility_mapper):
        letters = [deepcopy(tile.letter) for tile in tiles_in_hand]
        orientations = Orientation.values()

        if GameConfig.debug:
            print "calculate_best_move"
            board.pretty_print()
            print

        moves = []
        for coordinate in board.occupied_squares().keys():
            if GameConfig.debug:
                the_pusher[GameConfig.debug_channel].trigger('clear_debug')
            tile = board.get(coordinate).tile
            possible_words = self.lookup.find_words_using([tile.letter] + letters, 0)

            for orientation in orientations:
                for word in possible_words:
                    for move in self.valid_moves(coordinate, word, orientation, board):
                        moves.append(move)

        positive_scores = [move for move in moves if utility_mapper(tiles_in_hand, move.letters, self.state) > 0.0]

        if positive_scores:
            to_be_played = max(positive_scores, key=lambda ps: utility_mapper(tiles_in_hand, ps.letters, self.state))
            if GameConfig.debug:
                print to_be_played
            return PlaceMove(to_be_played.letters)
        else:
            return Pass()

    def think(self, tiles_in_hand, utility_mapper):
        # Game.instance
        board = self.state.playing_board
        if board.occupied_squares():
            return self.calculate_best_move(tiles_in_hand, board, utility_mapper)
        else:
            return self.calculate_first_move(tiles_in_hand, utility_mapper)
