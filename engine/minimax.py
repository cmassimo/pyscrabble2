from support import Move, PlaceMove, Pass, Game, Tile, Bag, Board, ComputerPlayer
from word_lookup import WordLookup
from config import Coordinate, Orientation, the_pusher, GameConfig, ScrabbleConfig

from copy import deepcopy
import time


class Minimax(object):
    def __init__(self, state, word_lookup, depth =3):
        self.lookup = word_lookup
        self.max_depth = depth
        # self.moves_score = {}
        self.moves = []
        self.scores = []
        self.state = state
        self.cut = False

    @staticmethod
    def utility_state(state):
        return state.current_player.score

    @staticmethod
    def apply_move(move, state):
        state.pass_count = 0

        if not move.is_valid:
            raise (InvalidMoveException("Move violates position requirements or forms one or more invalid words."))

        state.playing_board.put(move)

        state.current_player.add_score(move.score())

        state.current_player.tiles.remove_many([l for _, l in move.letters.items()])
        state.give_tiles(state.current_player, len(move.letters))

        state.move_count += 1
        state.current_player_index += 1
        if state.current_player_index >= len(state.players):
            state.current_player_index = 0

        # return state

    @staticmethod
    def duplicate_state(state):
        # dup state and clear associated objects
        new_state = deepcopy(state)
        new_state.players = []
        new_state._bag = Bag()
        new_state._board = Board()

        # dup players
        for cp in state.computer_players:
            new_cp = ComputerPlayer(cp.name, False)

            # dup player's tiles and attrs
            for t in cp.tiles:
                new_cp.tiles.append(Tile(t.letter))
                new_cp.score = cp.score
                new_cp.passes = cp.passes
                new_cp.utility_function = cp.utility_function

            new_state.players.append(new_cp)

        # dup bag tiles
        for t in state.tile_bag.inventory:
            new_state.tile_bag.inventory.append(Tile(t.letter))

        # dup board state
        length = ScrabbleConfig.board_length
        new_state.playing_board.grid = [ [ ScrabbleConfig.board_layout( Coordinate(i, j) ) for j in xrange(0, length) ] for i in xrange(0, length) ]

        # synch moves already done
        for i in range(0, length):
            for j in range(0, length):
                tile = state.playing_board.has_tile(Coordinate(i, j))
                if tile:
                    new_state.playing_board.put_tile_coord(Tile(tile.letter), Coordinate(i, j))

        return new_state

    def max_value(self, tiles_in_hand, utility_mapper, state, alpha, beta, depth):
        # print "-------------------------------------- MAX: %i" % depth
        # print [t.letter for t in tiles_in_hand]
        if depth == 0:
            util = self.utility_state(state)
            # if self.moves:
                # self.moves_score.setdefault(self.moves[0], util)
                # self.moves_score[self.moves[0]] = max(util, self.moves_score[self.moves[0]])
                # del self.moves[-1]
            if not self.cut:
                self.scores.append(util)
            self.cut = True

            return util
        # else:
        #     if len(self.moves) > 1:
        #         del self.moves[-1]

        v = -10000

        # print '==='
        # print [t.letter for t in tiles_in_hand]

        for succ, move in self.successors(state, tiles_in_hand, utility_mapper):
            tih = [Tile(t.letter) for t in succ.current_player.tiles]
            if depth == self.max_depth:
                self.moves.append(move)
            v = max(v, self.min_value(tih, utility_mapper, succ, alpha, beta, depth-1))

            if v >= beta:
                return v

            alpha = max(alpha, v)

            if depth == self.max_depth:
                self.cut = False

        return v

    def min_value(self, tiles_in_hand, utility_mapper, state, alpha, beta, depth):
        # print "-------------------------------------- MIN: %i" % depth
        # print [t.letter for t in tiles_in_hand]

        if depth == 0:
            util = self.utility_state(state)
            # if self.moves:
                # self.moves_score.setdefault(self.moves[0], util)
                # self.moves_score[self.moves[0]] = max(util, self.moves_score[self.moves[0]])
                # print self.moves_score
                # del self.moves[-1]
            if not self.cut:
                self.scores.append(util)
            self.cut = True

            return util
        # else:
        #     if len(self.moves) > 1:
        #         del self.moves[-1]

        v = 10000

        # print '==='
        # print [t.letter for t in tiles_in_hand]
        for succ, move in self.successors(state, tiles_in_hand, utility_mapper):
            tih = [Tile(t.letter) for t in succ.current_player.tiles]
            v = min(v, self.max_value(tih, utility_mapper, succ, alpha, beta, depth-1))

            if v <= alpha:
                return v

            beta = min(beta, v)
        
        return v

    def successors(self, state, tiles_in_hand, utility_mapper):
        if state.playing_board.occupied_squares():
            # state.playing_board.pretty_print()
            return ((self.gen_next_state_from_move(m, state), m) for m in self.next_possible_moves(tiles_in_hand, state, utility_mapper))
        else:
            return ((self.gen_next_state_from_move(m, state), m) for m in self.first_possible_moves(tiles_in_hand, state, utility_mapper))

    def gen_next_state_from_move(self, m, s):
        ns = self.duplicate_state(s)
        self.apply_move(m, ns)
        return ns

    def alpha_beta_search(self, tiles_in_hand, state, utility_mapper):
        score = self.max_value(tiles_in_hand, utility_mapper, self.duplicate_state(state), -10000, 10000, deepcopy(self.max_depth))

        # print self.moves
        # print self.scores

        if self.scores:
            max_score_index = self.scores.index(min(self.scores))
            if self.moves:
                to_be_played = self.moves[max_score_index]
            else:
                to_be_played = None
        else:
            to_be_played = None

        # if self.moves_score:
        #     to_be_played = max(self.moves_score.items(), key=lambda kv: kv[1])[0]
        # else:
        #     to_be_played = None

        if to_be_played:
            if GameConfig.debug:
                print to_be_played
            return PlaceMove(to_be_played.letters)
        else:
            return Pass()

    def possible_starts(self, word, horizontal):
        highest_start = max(0, (7 - len(word) + 1))

        starts = []
        for i in range(highest_start, 8):
            if horizontal:
                starts.append(Coordinate(i, 7))
            else:
                starts.append(Coordinate(7, i))

        return starts

    def first_possible_moves(self, tiles_in_hand, state, utility_mapper):
        possible_words = self.lookup.find_all_words([tile.letter for tile in tiles_in_hand])
        horizontal = [True, False]
        moves = []

        if GameConfig.debug:
            print "calculate_first_move"

        for o in horizontal:
            for word in possible_words:
                for start in self.possible_starts(word, o):
                    moves.append( Move( dict( [ (start.next(o, i), Tile(word.upper()[i])) for i in xrange(0, len(word)) ] ), state ) )

        fm = sorted([move for move in moves if utility_mapper(tiles_in_hand, move.letters, state) > 0.0], key=lambda i: -utility_mapper(tiles_in_hand, i.letters, state))
        return fm[0:self.max_depth-1]

    @staticmethod
    def valid_moves(c, word, o, board, state):
        letter = board.get(c).tile.letter

        unchecked_starts = []
        for i in range(0, len(word)):
            if word.upper()[i] == letter:
                if o == Orientation.horizontal:
                    if (c.x - i) >= 0 and (c.x + len(word) - i - 1) <= 14:
                        unchecked_starts.append( Coordinate(c.x - i, c.y) )
                else:
                    if (c.y - i) >= 0 and (c.y + len(word) - i - 1) <= 14:
                        unchecked_starts.append( Coordinate(c.x, c.y - i) )

        vmoves = []

        for start in unchecked_starts:
            coords_letters = []
            for i in range(0, len(word)):
                coord = start.next(o, i)
                if not board.has_tile(coord):
                    coords_letters.append( (coord, Tile(word.upper()[i])) )

            if coords_letters:
                move = Move(dict(coords_letters), state)
                if move.is_valid:
                    vmoves.append(move)
                    if GameConfig.debug:
                        the_pusher[GameConfig.debug_channel].trigger('debug', [{'x': c.x, 'y': c.y, 'tile': {'letter': t.letter, 'score': t.score}} for c, t in move.letters.items()])
                        time.sleep(1)
                        the_pusher[GameConfig.debug_channel].trigger('clear_debug')

        return vmoves

    def next_possible_moves(self, tiles_in_hand, state, utility_mapper):
        letters = [tile.letter for tile in tiles_in_hand]
        orientations = Orientation.values()
        board = state.playing_board

        if GameConfig.debug:
            print "calculate_best_move"
            board.pretty_print()
            print

        moves = []
        for coordinate in board.occupied_squares().keys():
            tile = board.get(coordinate).tile
            # print letters
            possible_words = self.lookup.find_words_using([tile.letter] + letters, 0)

            for orientation in orientations:
                for word in possible_words:
                    # print "POSSIBLE WORD: %s" % word
                    for move in self.valid_moves(coordinate, word, orientation, board, state):
                        moves.append(move)

        nps = sorted([move for move in moves if utility_mapper(tiles_in_hand, move.letters, state) > 0.0], key=lambda i: -utility_mapper(tiles_in_hand, i.letters, state))
        return nps[0:self.max_depth-1]

    def think(self, tiles_in_hand, utility_mapper):
        self.moves = []
        self.scores = []
        # print "tile bag len: %2i" % len(Game.instance.tile_bag.inventory)
        return self.alpha_beta_search(tiles_in_hand, self.state, utility_mapper)
