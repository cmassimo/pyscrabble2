from support import Move, PlaceMove, Pass, Game, Tile
from word_lookup import WordLookup
from config import Coordinate, Orientation

class MoveGenerator(object):
    def __init__(self, word_lookup):
        self.lookup = word_lookup

    def possible_starts(self, word, horizontal):
        self.highest_start = max(0, (7 - len(word) + 1))

        starts = []
        for i in range(self.highest_start, 8):
            if horizontal:
                starts.append(Coordinate(i, 7))
            else:
                starts.append(Coordinate(7, i))

        return starts

    def calculate_first_move(self, tiles_in_hand, utility_mapper):
        possible_words = self.lookup.find_all_words([tile.letter for tile in tiles_in_hand])
        horizontal = [True, False]
        moves = []

        print "Calculating moves for first move"
        print tiles_in_hand

        for o in horizontal:
            for word in possible_words:
                for start in self.possible_starts(word, o):
                    moves.append( Move( dict( [ (start.next(o, i), Tile(word.upper()[i])) for i in xrange(0, len(word)) ] ) ) )

        positive_scores = [move for move in moves if utility_mapper(tiles_in_hand, move.letters) > 0.0]

        if positive_scores:
            to_be_played = max(positive_scores, key=lambda ps: utility_mapper(tiles_in_hand, ps.letters))
            return PlaceMove(to_be_played.letters)
        else:
            return Pass()

    @staticmethod
    def valid_moves(c, word, o, board):
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
        letter_pos = []

        for start in unchecked_starts:
            for i in range(0, len(word)):
                coord = start.next(o, i)
                if not board.has_tile(coord):
                    letter_pos.append( (coord, Tile(word.upper()[i])) )

            if letter_pos:
                move = Move(dict(letter_pos))
                if move.is_valid:
                    vmoves.append(move)

        print "valid_moves len: %5i" % len(vmoves)
        return vmoves

    def calculate_best_move(self, tiles_in_hand, board, utility_mapper):
        letters = [tile.letter for tile in tiles_in_hand]
        orientations = Orientation.values()

        print "Calculating moves for best move"
        print tiles_in_hand
        
        moves = []
        for coordinate in board.occupied_squares():
            tile = board.get(coordinate).tile
            possible_words = self.lookup.find_words_using([tile.letter] + letters, 0)

            for orientation in orientations:
                for word in possible_words:
                    for move in self.valid_moves(coordinate, word, orientation, board):
                        moves.append(move)

        positive_scores = [move for move in moves if utility_mapper(tiles_in_hand, move.letters) > 0.0]

        if positive_scores:
            to_be_played = max(positive_scores, key=lambda ps: utility_mapper(tiles_in_hand, ps.letters))
            return PlaceMove(to_be_played.letters)
        else:
            return Pass()

    def think(self, tiles_in_hand, utility_mapper):
        board = Game.instance.playing_board
        if board.occupied_squares():
            return self.calculate_best_move(tiles_in_hand, board, utility_mapper)
        else:
            return self.calculate_first_move(tiles_in_hand, utility_mapper)
