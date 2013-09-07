class Square(object):
    def __init__(self, letter_mult, word_mult, gradient):
        self.letter_multiplier = letter_mult
        self.word_multiplier = word_mult
        self.gradient = gradient
        self.tile = None

    @property
    def letter_multiplier(self):
        if self.tile:
            return 1
        else:
            return self.letter_multiplier

    @property
    def word_multiplier(self):
        if self.tile:
            return 1
        else:
            return self.word_multiplier

    @property
    def tile(self):
        return self.tile

    @tile.setter
    def tile(self, t):
        self.tile = t

    @property
    def is_empty(self):
        return self.tile == None

    @property
    def gradient(self):
        return self.gradient

class NormalSquare(Square):
    def __init__(self):
        super().__init__(self, 1, 1, "FFFFFFFF")

class DoubleLetterSquare(Square):
    def __init__(self):
        super().__init__(self, 2, 1, "FF9696FF")

class TripleLetterSquare(Square):
    def __init__(self):
        super().__init__(self, 3, 1, "FF0000FE")

class DoubleWordSquare(Square):
    def __init__(self):
        super().__init__(self, 1, 2, "FFFF3C3C")

class TripleWordSquare(Square):
    def __init__(self):
        super().__init__(self, 1, 3, "FFFF0000")

class StartSquare(DoubleWordSquare):
    # def __init__(self):
    #     super().__init__(self)
    pass
