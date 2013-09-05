from random import shuffle, random

from config import ScrabbleConfig
from word_lookup import WordLookup

class Tile(object):
    @classmethod
    def __get_score(letter):
        l = letter.upper()
        
        if l in ['E', 'A', 'I', 'O', 'N', 'R', 'T', 'L', 'S', 'U']:
            return 1
        elif l in ['D', 'G']:
            return 2
        elif l in ['B', 'C', 'M', 'P']:
            return 3
        elif l in [ 'F', 'H', 'V',  'W', 'Y']:
            return 4
        elif l == 'K':
            return 5
        elif l in ['J', 'X']:
            return 8
        elif l in ['Q', 'Z']:
            return 10
        elif l == ' ':
            return 0
        else:
            raise (Exception("Only uppercase characters A - Z and a blank space are supported in Scrabble."))

    def __init__(self, letter):
        self.letter = letter
        self.score = Tile.__get_core(letter)

    def print(self):
        print "Letter: %c, Score: %i" % (self.letter, self.score)

    def __eq__(self, other):
        self.letter == other.letter

    # TODO
    def __cmp__(self, other):
        pass
        
    # TODO
    def __hash__(self, other):
        pass


class TileList(list):
    def __init__(self):
        list.__init__(self)

    def remove_many(self, tiles):
        # TODO could be improved performance-wise
        for t in tiles:
            el = next((x for x in self if x.letter == t.letter), None)
            if el:
                self.remove(el)
            else:
                raise (Exception(String.Format("Cannot remove tile '%c', it is not in the collection." % t.letter)))

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
    def __init__(self)
        self.pointer = 0
        self.inventory = []

        for k, v ScrabbleConfig.letter_quantity.items():
            for _ in range(0, v):
                self.inventory.append(Tile(k))

        shuffle(self.inventory)

    def is_empty(self):
        return len(inventory.keys()) == 0

    def print(self):
        for tile in inventory.values()
            tile.print()

    def take(self, n =1):
        if self.inventory:
            can_take = min(len(inventory.keys()), n)

            return [self.inventory.pop(i) for i in range(0, n)]
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
        implementor.perform_pass()

class DumpLetters(Turn):
    def __init__(self, tiles):
        self.letters = tiles

    def perform(self, implementor):
        implementor.perform_dump_letters()

class PlaceMove(Turn):
    def __init__(self, letters):
        self.letters = letters

    def perform(self, implementor):
        implementor.perform_move()


class Player(object):
    def __init__(self, name):
        self.name = name
        self.tiles = TileList()
        self.score = 0

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

    def take_turn(implementor, turn):
        implementor.take_turn(turn)

class GameOutcome(object):
    def __init__(self, winners):
        self.winners = winners

class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(self, name)

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(self, name)


# [<AbstractClass>]
# type Player(name:string) =
#     let tiles = TileList()
#     let mutable score = 0
#     abstract member NotifyTurn : ITurnImplementor -> unit
#     abstract member NotifyGameOver : GameOutcome -> unit
#     abstract member DrawTurn : Turn * Player -> unit
#     abstract member TilesUpdated : unit -> unit
#     member this.Name with get() = name
#     member this.Score with get() = score
#     member this.Tiles with get() = tiles
#     member this.HasTiles with get() = tiles.Count > 0
#     member this.AddScore(s) = 
#         score <- score + s
#     member this.FinalizeScore() =
#         score <- score - this.Tiles.Score()
#     member this.TakeTurn(implementor:ITurnImplementor, t:Turn) = 
#         implementor.TakeTurn(t)

# and GameOutcome(winners:seq<Player>) =
#     member this.Winners with get() = winners

# type ComputerPlayer(name:string) = 
#     inherit Player(name)

#     [<DefaultValue>] val mutable private window : IDispWindow
#     [<DefaultValue>] val mutable private provider : IIntelligenceProvider
#     member this.Provider with get() = this.provider and set x = this.provider <- x
#     [<DefaultValue>] val mutable private utility : TileList * Map<Coordinate, Tile> -> double
#     member this.UtilityFunction with get() = this.utility and set x = this.utility <- x

#     let mutable passes = 0

#     override this.NotifyTurn(implementor) =
#         if not(this.window = Unchecked.defaultof<IDispWindow>) then
#             let win = this.window :?> System.Windows.Threading.DispatcherObject
#             let f : del1 = new del1( fun () -> this.InvokeTurn(implementor) )
#             let st = System.Threading.ThreadStart(fun () -> win.Dispatcher.Invoke(System.Windows.Threading.DispatcherPriority.Normal, f) |> ignore)
#             let t = System.Threading.Thread(st)
#             t.Start()
#         else
#             this.InvokeTurn(implementor)
#     member this.InvokeTurn(implementor) =
#         let turn = this.provider.Think(this.Tiles, this.utility)
#         if turn.GetType().ToString() = "Scrabble.Core.Types.Pass" then
#             passes <- passes + 1
#         else
#             passes <- 0

#         if passes >= 3 && this.Tiles.Count = 7 then //auto-dump after 3 passes in a row, unless at the end of the game
#             passes <- 0
#             this.TakeTurn(implementor, DumpLetters(this.Tiles))
#         else
#             this.TakeTurn(implementor, turn)

#     member this.Window with get() = this.window and set w = this.window <- w

#     override this.NotifyGameOver(o:GameOutcome) = 
#         if not(this.window = Unchecked.defaultof<IDispWindow>) then
#             this.window.GameOver(o)
#     override this.DrawTurn(t:Turn, p:Player) = 
#         if not(this.window = Unchecked.defaultof<IDispWindow>) then
#             this.window.DrawTurn(t, p)
#     override this.TilesUpdated() = 
#         if not(this.window = Unchecked.defaultof<IDispWindow>) then
#             this.window.TilesUpdated()
# and IDispWindow = 
#     abstract member NotifyTurn : unit -> unit
#     abstract member DrawTurn : Turn * Player -> unit
#     abstract member Player : ComputerPlayer with get, set
#     abstract member GameOver : GameOutcome -> unit
#     abstract member TilesUpdated : unit -> unit
# and del1 = delegate of unit -> unit

# type HumanPlayer(name:string) =
#     inherit Player(name)
#     [<DefaultValue>] val mutable private window : IGameWindow
#     [<DefaultValue>] val mutable private game : ITurnImplementor
#     override this.NotifyTurn(implementor) = 
#         this.game <- implementor
#         this.window.NotifyTurn()
#     override this.NotifyGameOver(o:GameOutcome) = 
#         this.window.GameOver(o)
#     override this.DrawTurn(t:Turn, p:Player) = 
#         this.window.DrawTurn(t, p)
#     override this.TilesUpdated() = 
#         this.window.TilesUpdated()
#     member this.Window with get() = this.window and set w = this.window <- w
#     member this.TakeTurn(t:Turn) = 
#         base.TakeTurn(this.game, t)

# and IGameWindow =
#     abstract member NotifyTurn : unit -> unit
#     abstract member DrawTurn : Turn * Player -> unit
#     abstract member Player : HumanPlayer with get, set
#     abstract member GameOver : GameOutcome -> unit
#     abstract member TilesUpdated : unit -> unit

class Board(object):
    def __init__(self):
        length = ScrabbleConfig.board_length
        self.grid = [ [ ScrabbleConfig.board_layout( Coordinate(i, j) ) for j in xrange(0, length) ] for i in xrange(0, length) ]
                
    def get(self, coord):
        return self.get(coord.x, coord.y)

    def get(self, x, y):
        try:
            return self.grid[x][y]
        except:
            return None

    def has_tile(self, coord):
        return self.get(coord) == None

    def put(self, tile, coord):
        square = self.get(coord)
        if square:
            square.tile = tile

    def put(self, move):
        for c, t in move.letters.items():
            self.put(t, c)

    def occupied_squares(self):
        res = {}

        for i in range(0, len(self.grid[0])):
            for j in range(0, len(self.grid)):
                s = self.grid[i][j]
                if s.tile:
                    res[Coordinate(i, j)] = s

        return res

    def has_neighbouring_tile(self, coord):
        return any([ self.has_tile(n) for n in coord.neighbors() ])

    def pretty_print(self):
        print "   "
        for j in range(0, len(self.grid)):
            printf "%2i " % j
        print ""

        for i in range(0, len(self.grid[0])):
            printf "%2i " % i
            for j in range(0, len(self.grid)):
                s = self.grid[j][i]
                if s.tile:
                    tile = s.tile
                    printf " %s " % tile.letter
                else:
                    print " _ "
            print ""

class GameState(object):
    def __init__(self, players):
        self.players = players
        self.bag = Bag()
        self.board = Board()
        self.move_count = 0
        # self.rng = random()
        self.current_player_index = 0
        self.pass_count = 0
        self.word_lookup = WordLookup()

    def is_game_complete(self):
        return any([not p.has_tiles for p in self.players])
            or (self.pass_count == len(self.players)*2)
            or ((not self.bag) and self.pass_count == len(self.players))

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
        o = GameOutcome(self.winning_players())
        # players |> List.iter (fun p -> p.NotifyGameOver(o))

    class TurnImplementor:
        def __init__(self, game_state):
            self.gs = game_state

        def perform_pass(self):
            self.gs.pass_count += 1

        def perform_dump_letters(self, dl):
            self.gs.pass_count = 0
            letters = dl.letters.sort()

            self.gs.current_player().tiles.remove_many(letters)

            self.gs.bag.put(letters)
            self.gs.give_tiles(self.gs.current_player(), len(letters))

        def perform_move(self, turn):
            self.gs.pass_count = 0
            move = Move(turn.letters)
            if not move.is_valid():
                raise (InvalidMoveException("Move violates position requirements or forms one or more invalid words."))

            self.gs.board.put(move)
            self.gs.current_player().add_score(move.score)
            self.gs.current_player().tiles.remove_many([l for _, l in turn.letters])
            self.give_tiles(self.gs.current_player(), len(turn.letters))

        def take_turn(self, turn):
            turn.perform(self)
            for player in self.gs.other_players():
                player.draw_turn(turn, self.gs.current_player())

            if not self.gs.is_game_complete():
                if self.gs.is_opening_move() and not (type(turn) == PlaceMove):
                    self.gs.move_count -= 1

                self.gs.next_move()
            else:
                self.gs.finish_game()

    @property
    def tile_bag(self):
        return self.bag

    @property
    def playing_board(self):
        return self.board

    @property
    def move_count(self):
        return self.move_count

    @move_count.setter
    def move_count(self, count):
        self.move_count = count

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
        if self.current_player_index >= len(self.playersobject):
            self.current_player_index = 0

        self.current_player().notify_turn(self)

    def other_players(self):
        return [self.players[i] for i in len(self.players) if i != self.current_player_index]

    def give_tiles(player, n):
        if self.bag:
            new_tiles = self.bag.take(n)
            player.tiles.extend(new_tiles)
            player.tiles_updated()

    def start(self):
        for player in self.players:
            player.tiles.extend(self.bag.take ScrabbleConfig.max_tiles)
            player.tiles_updated()

        self.current_player().notify_turn(self)

"""Singleton representing the game board, bag of tiles, players, move count, etc."""
class Game(object):
    instance = None # should be the GameState

"""
    A player's move is a set of coordinates and tiles. This will throw if the move isn't valid.
    That is, if the tiles aren't layed out properly (not all connected, the word formed doesn't "touch" any other tiles - with the exception of the first word)
    and if there is a "run" of connected tiles that doesn't form a valid word
"""
class Move(object):
    def __init__(self, letters):
        self.letters = letters # [<coord, tile>, ...]

        self.sorted = [(c, t) for c, t in self.letters.items()].sort(key=c)
        self.first = self.sorted[0][0]
        self.last = self.sorted[-1][0]

    def check_board_prev(self, coord, orientation):
        prev = coord.prev(orientation)
        return prev.is_valid() and Game.instance.playing_board().has_tile(prev)

    def check_board_next(self, coord, orientation):
        next = coord.next(orientation)
        return next.is_valid() and Game.instance.playing_board().has_tile(next)

    def range(self):
        try:
            Coordinate.between(self.first, self.last)
        except UnsupportedCoordinateException as e:
            raise InvalidMoveException(e.strerror)

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
        not any([Game.instance.has_tile(coord) for coord, _ in self.letters.items()])

    def check_move_occupied(self, coord):
        return (coord in self.letters.keys()) or Game.instance.has_tile(coord)

    def opposite(self, orientation):
        return (orientation + 1) % 1

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
        return any([ Game.instance.has_tile(c) or Game.instance.playing_board.has_neighbouring_tile(c) for c in self.range() ])

    def contains_start_square(self):
        return ScrabbleConfig.start_coordinate in self.letters.keys()

    def valid_placement(self):
        return self.not_overwriting_tiles() and self.is_aligned() and self.is_consecutive()
            and (Game.instance.is_opening_move() and self.contains_start_square())
            or (not Game.instance.is_opening_move() and self.is_connected())

    def compute_runs(self):
        alt = self.opposite(self.orientation())
        alternate_runs = [Run(c, alt, self.letters) for c, _ in self.sorted]
        return [Run(self.first, self.orientation(), self.letters)] + alternate_runs

    def valid_runs(self, runs):
        return all([r.is_valid() for r in runs])

    def compute_score(self, runs):
        score = reduce(lambda r: r.score, runs)

        if len(self.letters) == ScrabbleConfig.max_tiles:
            return score + ScrabbleConfig.all_tiles_bonus
        else:
            return score

    def score(self):
        if self.valid_placement():
            runs = self.compute_runs()
            if self.valid_runs(runs):
                return self.compute_score(runs)
            else:
                return -1 # raise (InvalidMoveException("One or more invalid words were formed by this move."))
        else:
            return -1 # raise (InvalidMoveException("Move violates positioning rules (i.e. not connected to other tiles)."))

    def valid(self):
        return self.score() >= 0

    @property
    def is_valid(self):
        return self.valid()

    def __str__(self):
        tpl = "%c : (%2i, %2i)\n"
        if len(self.letters) > 1:
            return ''.join([tpl % (l[1].letter, l[0].x, l[0].y) for l in self.letters.items()])
        else:
            l = self.letters.items()[0]
            return tpl % (l[1].letter, l[0].x, l[0].y)

class Run(object):
    def __init__(self, coord, orientation, move_letters):
        self.coordinate = coord
        self.orientation = orientation
        self.move_letters = move_letters

    def get_tile_from_move(self, coord):
        if coord in self.move_letters.keys():
            return move_letters[coord]
        else:
            return Game.instance.playing_board().get(coord).tile

    def check(self, coord, orientation, increment):
        if not coord.is_valid():
            return []
        else:
            square = Game.instance.playing_board().get(coord)
            tile = self.get_tile_from_move(coord)
            if tile:
                next = increment(coord, orientation)
                return [(square, tile)] + self.check(next, orientation, increment)
            else:
                return []

    def prev_squares(self):
        return self.check(self.coordinate, self.orientation, lambda c, o: c.prev(o))

    def next_squares(self):
        return self.check(self.coordinate, self.orientation, lambda c, o: c.next(o))

    def squares(self):
        return list(reversed(self.prev_squares())) + self.next_squares()

    def length(self):
        return len(self.squares())

    def to_word(self):
        return ''.join([t.letter for t in [t for _, t in self.squares()]])

    def is_valid(self):
        return Game.instance.dictionary().is_valid_word(self.to_word())

    def score(self):
        word_mult = reduce(lambda x, y: x*y, [s.word_multiplier for s, _ in self.squares], 1)
        letter_score = sum([s.letter_multiplier*t.score for s, t in self.squares])
        return word_mult*letter_score
