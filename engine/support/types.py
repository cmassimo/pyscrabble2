from random import shuffle
import json
import hashlib
import datetime

from exceptions import *
from config import ScrabbleConfig, Coordinate, Orientation, the_pusher, GameConfig
from word_lookup import WordLookup

class ObjEncoder(json.JSONEncoder):
    def default(self, obj):
        std = [dict, list, tuple, str, unicode, int, long, float, True, False, None]

        if type(obj) in std :
            return super(ObjEncoder, self).default(obj)

        res = obj.__dict__
        res.setdefault('type', type(obj).__name__)
        return res

class Tile(object):
    @classmethod
    def __get_score(cls, letter):
        l = letter.upper()
        
        # en
        # if l in ['E', 'A', 'I', 'O', 'N', 'R', 'T', 'L', 'S', 'U']:
        #     return 1
        # elif l in ['D', 'G']:
        #     return 2
        # elif l in ['B', 'C', 'M', 'P']:
        #     return 3
        # elif l in [ 'F', 'H', 'V',  'W', 'Y']:
        #     return 4
        # elif l == 'K':
        #     return 5
        # elif l in ['J', 'X']:
        #     return 8
        # elif l in ['Q', 'Z']:
        #     return 10
        # elif l == ' ':
        #     return 0
        # else:
        #     raise (Exception("Only uppercase characters A - Z and a blank space are supported in Scrabble."))

        if l in ['E', 'A', 'I', 'O']:
            return 1
        elif l in ['C', 'R', 'S', 'T']: 
            return 2
        elif l in ['L', 'M', 'N', 'U']:
            return 3
        elif l in ['B', 'D', 'F', 'P', 'V']:
            return 5
        elif l in ['G', 'H', 'Z']:
            return 8
        elif l == 'Q':
            return 10
        elif l == ' ':
            return 0
        else:
            raise (Exception("Only uppercase characters A - Z and a blank space are supported in Scrabble."))

    def __init__(self, letter):
        self.letter = letter
        self.score = Tile.__get_score(letter)

    def __str__(self):
        return "Letter: %c, Score: %i" % (self.letter, self.score)

    __repr__ = __str__

    def __eq__(self, other):
        return self.letter == other.letter

    def __cmp__(self, other):
        if self.letter == other.letter:
            return 0
        elif self.letter > other.letter:
            return 1
        elif self.letter < other.letter:
            return -1

    def __hash__(self):
        return self.letter.__hash__()

class TileList(list):
    def __init__(self):
        list.__init__(self)

# che vedemo: ala
# ['Q', 'L', 'E', 'I', 'A', 'E', 'I']
# ['L', 'L', 'A', 'A']
# can't remove L si ma quale

    def remove_many(self, tiles):
        # print 'remove_many:'
        # print [t1.letter for t1 in self]
        for t in tiles:
            # print t.letter
            if t in self:
                self.remove(t)
            else:
                raise Exception("Cannot remove tile '%c', it is not in the collection." % t.letter)
            # el = next((x for x in self if x.letter == t.letter), None)
            # if el:
            #     self.remove(el)
            # else:
            #     raise Exception("Cannot remove tile '%c', it is not in the collection." % t.letter)

    def shuffle(self):
        shuffle(self)

    def score(self):
        return reduce(lambda x, tile: x + tile.score, self, 0)

    def draw(self, n):
        res = self[0:n]
        del self[0:n]
        return res

    def take_char(c):
        el = next((x for x in self if x.letter == c), None)
        if el:
            self.remove(el)
            return Tile(c)
        else:
            raise (Exception("Tile was not found in the list."))

    def has_equal_elements(self, other):
        if len(self) == len(other):
            for i in len(self):
                if self[i] != other[i]:
                    break
            else:
                return True

            return False
        else:
            return False

    def __eq__(self, other):
        if type(other) == type(self):
            return self.has_equal_elements(other)
        else:
            return False

class Bag(object):
    def __init__(self):
        self.pointer = 0
        self.inventory = []

        for k, v in ScrabbleConfig.letter_quantity.items():
            for _ in range(0, v):
                self.inventory.append(Tile(k))

        shuffle(self.inventory)

    def is_empty(self):
        return len(self.inventory) == 0

    def __str__(self):
        return "\n".join([tile.__str__() for tile in self.inventory])

    def take(self, n =1):
        if self.inventory:
            can_take = min(len(self.inventory), n)

            taken = [self.inventory[i] for i in range(0, can_take)]
            del self.inventory[0:can_take]

            return taken
        else:
            raise (Exception("The bag is empty, you can not take any tiles."))

    def put(self, tiles):
        self.inventory += tiles
        shuffle(self.inventory)

class Turn(object):
    def perform(self):
        raise NotImplementedError( "abstract method called: needs implementation" )

class Pass(Turn):
    def perform(self, implementor):
        return implementor.perform_pass()

class DumpLetters(Turn):
    def __init__(self, tiles):
        self.letters = [Tile(t.letter) for t in tiles]

    def perform(self, implementor):
        return implementor.perform_dump_letters(self)

class PlaceMove(Turn):
    def __init__(self, letters):
        self.letters = letters

    def perform(self, implementor):
        return implementor.perform_move(self)


class Player(object):
    def __init__(self, name, web =True):
        self.name = name
        # str((datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds())
        self.pid = hashlib.md5(name + str(datetime.datetime.now())).hexdigest()[0:6]
        self.tiles = TileList()
        self.score = 0
        self.web = web

    def notify_turn(self, game_state):
        raise NotImplementedError( "abstract method called: needs implementation" )

    def notify_game_over(self):
        raise NotImplementedError( "abstract method called: needs implementation" )

    def draw_turn(self):
        raise NotImplementedError( "abstract method called: needs implementation" )

    def tiles_updated(self):
        raise NotImplementedError( "abstract method called: needs implementation" )

    def has_tiles(self):
        return len(self.tiles) > 0

    def add_score(self, score):
        self.score += score

    def finalize_score(self):
        self.score -= reduce(lambda x, tile: x + tile.score, self.tiles, 0)

    @staticmethod
    def take_turn(implementor, turn):
        return implementor.take_turn(turn)

    def is_human(self):
        return False

    def summary(self):
        return {'pid': self.pid, 'name': self.name, 'score': self.score, 'tiles': [{'letter': t.letter, 'score': t.score} for t in self.tiles]}

class GameOutcome(object):
    def __init__(self, winners, all_updated_players):
        self.winners = winners
        self.all_updated_players = all_updated_players

    def summary(self):
        return {'winners': [w.summary() for w in self.winners], 'all_players': [a.summary() for a in self.all_updated_players]}

class ComputerPlayer(Player):
    def __init__(self, name, web =True):
        super(ComputerPlayer, self).__init__(name, web)
        self.passes = 0
        self.channel = 'computer_' + str(self.pid)

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, provider):
        self._provider = provider

    @property
    def utility_function(self):
        return self.utility

    @utility_function.setter
    def utility_function(self, func):
        self.utility = func

    def notify_turn(self, implementor):
        return self.invoke_turn(implementor)

    def invoke_turn(self, implementor):
        turn = self.provider.think(self.tiles, self.utility)

        if type(turn) == Pass:
            self.passes += 1
        else:
            self.passes = 0

        # auto-dump after 3 passes in a row, unless at the end of the game
        if self.passes > 3 and len(self.tiles) == ScrabbleConfig.max_tiles:
            self.passes = 0
            return self.take_turn(implementor, DumpLetters(self.tiles))
        else:
            return self.take_turn(implementor, turn)

    def notify_game_over(self, go):
        data = {'game_outcome': go.summary()}
        if self.web:
            the_pusher[self.channel].trigger('game_over', data)
        else:
            if go.winners:
                return (go.winners[0].provider.__class__.__name__, go.winners[0].utility.__name__)
            else:
                return ("", "")
            # print "********************************* game_over: %s" % go.summary()

    def draw_turn(self, turn, player, s):
        data = {'player': player.summary(), 'string': s}
        if type(turn) == PlaceMove:
            data['move'] = [{'x': c.x, 'y': c.y, 'tile': {'letter': t.letter, 'score': t.score}} for c, t in turn.letters.items()]
        if self.web:
            the_pusher[self.channel].trigger('draw_turn', data)
        else:
            pass
            # print "********************************* draw_turn: %s self.passes: %2i" % (s, self.passes)

    def tiles_updated(self):
        if self.web:
            data = {'tiles': [{'letter': t.letter, 'score': t.score} for t in self.tiles]}
            the_pusher[self.channel].trigger('tiles_updated', data)
        else:
            pass
            # print "********************************* tiles_updated: %2i" % self.passes

class HumanPlayer(Player):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)
        self.channel = 'human'

    def notify_turn(self, implementor):
        self.game = implementor
        the_pusher[self.channel].trigger('notify_turn')

    def notify_game_over(self, go):
        data = {'game_outcome': go.summary()}
        the_pusher[self.channel].trigger('game_over', data)

    def draw_turn(self, turn, player, s):
        data = {'player': player.summary(), 'string': s}
        the_pusher[self.channel].trigger('draw_turn', data)

    def tiles_updated(self):
        the_pusher[self.channel].trigger('tiles_updated')

    def take_turn(implementor, turn):
        super(HumanPlayer, self).take_turn(self.game, turn)

    def is_human(self):
        return True


class Board(object):
    def __init__(self):
        length = ScrabbleConfig.board_length
        self.grid = [ [ ScrabbleConfig.board_layout( Coordinate(i, j) ) for j in xrange(0, length) ] for i in xrange(0, length) ]
                
    def get(self, coord):
        return self.get_xy(coord.x, coord.y)

    def get_xy(self, x, y):
        try:
            return self.grid[x][y]
        except:
            return None

    def has_tile(self, coord):
        return self.get(coord).tile

    def put_tile_coord(self, tile, coord):
        square = self.get(coord)
        if square:
            square.tile = tile

    def put(self, move):
        for c, t in move.letters.items():
            self.put_tile_coord(t, c)

    def occupied_squares(self):
        res = {}

        for i in range(0, ScrabbleConfig.board_length):
            for j in range(0, ScrabbleConfig.board_length):
                s = self.grid[i][j]
                if s.tile:
                    res[Coordinate(i, j)] = s

        return res

    def has_neighbouring_tile(self, coord):
        return any([ self.has_tile(n) for n in coord.neighbors() ])

    def pretty_print(self):
        header = "   "
        for j in range(0, len(self.grid)):
            header += "%2i " % j
        print header

        for i in range(0, len(self.grid[0])):
            row = "%2i " % i
            for j in range(0, len(self.grid)):
                s = self.grid[j][i]
                if s.tile:
                    tile = s.tile
                    row += " %s " % tile.letter
                else:
                    row += " _ "
            print row

class GameState(object):
    def __init__(self, word_lookup, players):
        self.players = players
        self._bag = Bag()
        self._board = Board()
        self._move_count = 0
        self.running = False
        self.current_player_index = 0
        self.pass_count = 0
        self.word_lookup = word_lookup

    def is_game_complete(self):
        return (any([not p.has_tiles() for p in self.players]) or
            (self.pass_count == len(self.players)*2)  or
            ((not self._bag.is_empty) and self.pass_count == len(self.players))) or (GameConfig.debug and self._move_count >= GameConfig.max_moves)

    def finalize_scores(self):
        for player in self.players:
            player.finalize_score()

        bonus = sum([ reduce(lambda x, tile: x + tile.score, player.tiles, 0) for player in self.players if player.has_tiles])

        for player in self.players:
            if not player.has_tiles:
                player.add_score(bonus)

    def winning_players(self):
        max_score_player = max(self.players, key=lambda p: p.score)
        return [player for player in self.players if player.score == max_score_player.score]

    def finish_game(self):
        self.finalize_scores()
        go = GameOutcome(self.winning_players(), self.players)
        winners = self.winning_players()
        # for p in self.players:
        # if winners:
        #     return winners[0].notify_game_over(go)

        return self.players[0].notify_game_over(go)


    class TurnImplementor:
        def __init__(self, game_state):
            self.gs = game_state

        def perform_pass(self):
            self.gs.pass_count += 1
            return self.gs.current_player.name + " passa il turno.";

        def perform_dump_letters(self, dl):
            
            self.gs.pass_count = 0
            letters = sorted(dl.letters)

            self.gs.current_player.tiles.remove_many(letters)

            self.gs.tile_bag.put(letters)
            self.gs.give_tiles(self.gs.current_player, len(letters))

            return self.gs.current_player.name + " ha cambiato lettere.";

        def perform_move(self, turn):
            self.gs.pass_count = 0
            move = Move(turn.letters, self.gs)

            if not move.is_valid:
                raise InvalidMoveException("Move violates position requirements or forms one or more invalid words.")

            self.gs.playing_board.put(move)
            self.gs.current_player.add_score(move.score())
            self.gs.current_player.tiles.remove_many([l for _, l in turn.letters.items()])
            self.gs.give_tiles(self.gs.current_player, len(turn.letters))

            return self.gs.current_player.name + " totalizza " + str(move.score()) + " punti con: " + ''.join([t.letter for _, t in move.letters.items()]);

        def take_turn(self, turn):
            summary = turn.perform(self)
            self.gs.current_player.draw_turn(turn, self.gs.current_player, summary)

            # for player in self.gs.other_players():
                # player.draw_turn(turn, self.gs.current_player, summary)

            if not self.gs.is_game_complete():
                if self.gs.is_opening_move and not (type(turn) == PlaceMove):
                    self.gs.move_count -= 1

                return self.gs.next_move()
            else:
                return self.gs.finish_game()

    @property
    def tile_bag(self):
        return self._bag

    @property
    def playing_board(self):
        return self._board

    @property
    def move_count(self):
        return self._move_count

    @move_count.setter
    def move_count(self, count):
        self._move_count = count

    @property
    def is_opening_move(self):
        return self.move_count == 0

    @property
    def human_players(self):
        return [player for player in self.players if type(player) is HumanPlayer]

    @property
    def computer_players(self):
        return [player for player in self.players if type(player) is ComputerPlayer]

    @property
    def dictionary(self):
        return self.word_lookup

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def next_move(self):
        self.move_count += 1
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0

        return self.current_player.notify_turn(self.TurnImplementor(self))

    def other_players(self):
        return [self.players[i] for i in range(0, len(self.players)) if i != self.current_player_index]

    def give_tiles(self, player, n):
        if not self._bag.is_empty():
            new_tiles = self._bag.take(n)
            player.tiles.extend(new_tiles)
        player.tiles_updated()

    def start(self):
        print "START"
        self.running = True

        for player in self.players:
            player.tiles.extend(self._bag.take(ScrabbleConfig.max_tiles))
            player.tiles_updated()

        return self.current_player.notify_turn(self.TurnImplementor(self))

    def continue_game(self):
        if not self.running:
            return self.start()
        elif self.current_player.is_human:
            self.current_player.notify_turn(self.TurnImplementor(self))

"""Singleton representing the game board, bag of tiles, players, move count, etc."""
class Game(object):
    # loader = None # should be the GameState
    instance = None

    # @classmethod
    # def instance(cls):
    #     cls.loader.load()

"""
    A player's move is a set of coordinates and tiles. This will throw if the move isn't valid.
    That is, if the tiles aren't layed out properly (not all connected, the word formed doesn't "touch" any other tiles - with the exception of the first word)
    and if there is a "run" of connected tiles that doesn't form a valid word
"""
class Move(object):
    def __init__(self, letters, state):
        self.letters = letters # [<coord, tile>, ...]

        self.sorted = sorted([(c, t) for c, t in self.letters.items()], key=lambda (c,t): c)
        self.first = self.sorted[0][0]
        self.last = self.sorted[-1][0]
        self._score = None
        self._state = state


    def check_board_prev(self, coord, orientation):
        prev = coord.prev(orientation)
        return prev.is_valid() and self._state.playing_board.has_tile(prev)

    def check_board_next(self, coord, orientation):
        next = coord.next(orientation)
        return next.is_valid() and self._state.playing_board.has_tile(next)

    def range(self):
        try:
            return Coordinate.between(self.first, self.last)
        except UnsupportedCoordinateException as e:
            raise InvalidMoveException(e.args[0])

    def orientation(self):
        if len(self.letters.items()) == 1:
            if self.check_board_next(self.first, Orientation.vertical) or self.check_board_prev(self.first, Orientation.vertical):
                return Orientation.vertical
            else:
                return Orientation.horizontal
        elif self.first.x == self.last.x:
            return Orientation.vertical
        else:
            return Orientation.horizontal

    def not_overwriting_tiles(self):
        return not any([self._state.playing_board.has_tile(coord) for coord, _ in self.letters.items()])

    def check_move_occupied(self, coord):
        return (coord in self.letters.keys()) or self._state.playing_board.has_tile(coord)

    def opposite(self, orientation):
        return (orientation + 1) % 2

    def is_aligned(self):
        if len(self.letters) <= 1:
            return True
        else:
            c0 = self.letters.keys()[0]
            v = all([c0.x == c.x for c, t in self.letters.items()])
            h = all([c0.y == c.y for c, t in self.letters.items()])
            return (v or h)

    def is_consecutive(self):
        return all([ self.check_move_occupied(c) for c in self.range() ])

    def is_connected(self):
        return any([ self._state.playing_board.has_tile(c) or self._state.playing_board.has_neighbouring_tile(c) for c in self.range() ])

    def contains_start_square(self):
        return ScrabbleConfig.start_coordinate() in self.letters.keys()

    def valid_placement(self):
        return (self.not_overwriting_tiles() and self.is_aligned() and self.is_consecutive() and
            (self._state.is_opening_move and self.contains_start_square()) or
            (not self._state.is_opening_move and self.is_connected()))

        # res = self.not_overwriting_tiles()
        # print res
        # res = res and self.is_aligned()
        # print res
        # res = res and self.is_consecutive()
        # print res
        # res2 = res and Game.instance.is_opening_move and self.contains_start_square()
        # print res2
        # res3 = res and not Game.instance.is_opening_move and self.is_connected()
        # print res3
        # print '----'

        return res and (res2 or res3)

    def compute_runs(self):
        alt = self.opposite(self.orientation())

        alternate_runs = [Run(c, alt, self.letters, self._state) for c, _ in self.sorted]
        alternate_runs = [a for a in alternate_runs if a.length() > 1]

        return [Run(self.first, self.orientation(), self.letters, self._state)] + alternate_runs

    def valid_runs(self, runs):
        return all([r.is_valid() for r in runs])

    def compute_score(self, runs):
        score = reduce(lambda x, r: r.score(), runs, 0)

        if len(self.letters) == ScrabbleConfig.max_tiles:
            return score + ScrabbleConfig.all_tiles_bonus
        else:
            return score

    def score(self):
        if not self._score:
            if self.valid_placement():
                runs = self.compute_runs()
                if self.valid_runs(runs):
                    self._score = self.compute_score(runs)
                else:
                    self._score = -1 # raise (InvalidMoveException("One or more invalid words were formed by this move."))
            else:
                self._score = -1 # raise (InvalidMoveException("Move violates positioning rules (i.e. not connected to other tiles)."))

        return self._score

    def valid(self):
        return self.score() >= 0

    @property
    def is_valid(self):
        return self.valid()

    def __str__(self):
        tpl = "%c : (%2i, %2i)\n"
        if len(self.sorted) > 1:
            return ''.join([tpl % (l[1].letter, l[0].x, l[0].y) for l in self.sorted])
        else:
            l = self.sorted[0]
            return tpl % (l[1].letter, l[0].x, l[0].y)

    __repr__ = __str__

class Run(object):
    def __init__(self, coord, orientation, move_letters, state):
        self.coordinate = coord
        self.orientation = orientation
        self.move_letters = move_letters
        self._state = state

    def get_tile_from_move(self, coord):
        if coord in self.move_letters.keys():
            return self.move_letters[coord]
        else:
            return self._state.playing_board.get(coord).tile

    def check(self, coord, orientation, increment):
        if not coord.is_valid():
            return []
        else:
            square = self._state.playing_board.get(coord)
            tile = self.get_tile_from_move(coord)
            if tile:
                next = increment(coord, orientation)
                return [(square, tile)] + self.check(next, orientation, increment)
            else:
                return []

    def prev_squares(self):
        return self.check(self.coordinate, self.orientation, lambda c, o: c.prev(o))

    def next_squares(self):
        return self.check(self.coordinate.next(self.orientation), self.orientation, lambda c, o: c.next(o))

    def squares(self):
        return list(reversed(self.prev_squares())) + self.next_squares()

    def length(self):
        return len(self.squares())

    def to_word(self):
        return ''.join([t.letter for t in [t for _, t in self.squares()]])

    def is_valid(self):
        return self._state.dictionary.is_valid_word(self.to_word())

    def score(self):
        word_mult = reduce(lambda x, y: x*y, [s.word_multiplier for s, _ in self.squares()], 1)
        letter_score = sum([s.letter_multiplier*t.score for s, t in self.squares()])
        return word_mult*letter_score
