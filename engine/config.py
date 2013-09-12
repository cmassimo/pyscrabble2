from exceptions import *
import os

from pusher import Pusher

from squares import *

WORDLIST_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../twl.txt"
DEBUG = False
MAX_MOVES = 6
DEBUG_CHANNEL = ''

the_pusher = Pusher(
    app_id='53591',
    key='a0a56b5e372395197020',
    secret='0f0db5e609af25a002c3'
)

class Orientation(object):
    vertical = 0
    horizontal = 1

    def __init__(self):
        raise Exception("This class is an ENUM and can't be instantiated")

    @classmethod
    def values(cls):
        return [cls.vertical, cls.horizontal]

class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%2i, %2i)" % (self.x, self.y)

    __repr__ = __str__

    def neighbors(self):
        nb = []
        if self.valid_xy(self.x - 1):
            nb.append(Coordinate(self.x - 1, self.y))
        if self.valid_xy(self.y - 1):
            nb.append(Coordinate(self.x, self.y - 1))
        if self.valid_xy(self.x + 1):
            nb.append(Coordinate(self.x + 1, self.y))
        if self.valid_xy(self.y + 1):
            nb.append(Coordinate(self.x, self.y + 1))

        return nb

    def is_valid(self):
        return self.valid_xy(self.x) and self.valid_xy(self.y)

    def next(self, orientation, offset =1):
        if orientation == Orientation.horizontal:
            return Coordinate(self.x + offset, self.y)
        else:
            return Coordinate(self.x, self.y + offset)

    def prev(self, orientation):
        if orientation == Orientation.horizontal:
            return Coordinate(self.x - 1, self.y)
        else:
            return Coordinate(self.x, self.y - 1)

    @staticmethod
    def between(c0, c1):
        first = min(c0, c1)
        last = max(c0, c1)

        if first.x == last.x:
            return [Coordinate(first.x, y) for y in xrange(first.y, last.y+1)]
        elif first.y == last.y:
            return [Coordinate(x, first.y) for x in xrange(first.x, last.x+1)]
        else:
            raise UnsupportedCoordinateException("Coordinates are not on the same axis.")

    @staticmethod
    def valid_xy(i):
        return i >= 0 and i < ScrabbleConfig.board_length

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __cmp__(self, other):
        cmp_x = self.x.__cmp__(other.x)
        if not cmp_x:
            return self.y.__cmp__(other.y)
        else:
            return cmp_x

    def __hash__(self):
        return self.x.__hash__() + self.y.__hash__()
        # return int(str(self.x) + str(self.y))

class ScrabbleConfig(object):
    letter_quantity = {'A': 9, 'C': 2, 'B': 2, 'E': 12, 'D': 4, 'G': 3, 'F': 2, 'I': 9, 'H': 2, 'K': 1, 'J': 1, 'M': 2, 'L': 4, 'O': 8, 'N': 6, 'Q': 1, 'P': 2, 'S': 4, 'R': 6, 'U': 4, 'T': 6, 'W': 2, 'V': 2, 'Y': 2, 'X': 1, 'Z': 1}
    max_tiles = 7
    all_tiles_bonus = 50
    board_length = 15
    
    @staticmethod
    def start_coordinate():
        return Coordinate(7, 7)

    @staticmethod
    def board_layout(c):
        if (c.x, c.y) in [(0, 0), (0, 7), (0, 14), (7, 0), (14, 0), (7, 14), (14, 7), (14, 14)]:
            return TripleWordSquare()
        elif (c.x, c.y) in [(5, 1), (9, 1), (1, 5), (5, 5), (9, 5), (13, 5), (1, 9), (5, 9),
            (9, 9), (13, 9), (5, 13), (9, 13)]:
            return TripleLetterSquare()
        elif (c.x, c.y) in [(1, 1), (2, 2), (3, 3), (4, 4), (10, 4), (11, 3), (12, 2), (13, 1),
            (1, 13), (2, 12), (3, 11), (4, 10), (13, 13), (10, 10), (12, 12), (11, 11)]:
            return DoubleWordSquare()
        elif (c.x, c.y) in [(3, 0), (11, 0), (6, 2), (8, 2), (0, 3), (7, 3), (14, 3), (2, 6), (6, 6), (8, 6), (12, 6), (3, 7), (11, 7), (2, 8), (6, 8), (8, 8), (12, 8), (0, 11), (7, 11), (14, 11), (6, 12), (8, 12), (3, 14), (11, 14)]:
            return DoubleLetterSquare()
        elif (c.x, c.y) == (7, 7):
            return StartSquare()
        else:
            return NormalSquare()
