class Square(object):
    def __init__(self, letter_mult, word_mult, css_class):
        self._letter_multiplier = letter_mult
        self._word_multiplier = word_mult
        self.css_class = css_class
        self._tile = None

    @property
    def letter_multiplier(self):
        if self.tile:
            return 1
        else:
            return self._letter_multiplier

    @letter_multiplier.setter
    def letter_multiplier(self, lm):
        self._letter_multiplier = lm

    @property
    def word_multiplier(self):
        if self.tile:
            return 1
        else:
            return self._word_multiplier

    @word_multiplier.setter
    def word_multiplier(self, wm):
        self._word_multiplier = wm

    @property
    def tile(self):
        return self._tile

    @tile.setter
    def tile(self, t):
        self._tile = t

    @property
    def is_empty(self):
        return self.tile == None

    @property
    def gradient(self):
        return self._gradient

class NormalSquare(Square):
    def __init__(self):
        super(NormalSquare, self).__init__(1, 1, "")

class DoubleLetterSquare(Square):
    def __init__(self):
        super(DoubleLetterSquare, self).__init__(2, 1, "doubleLetter")

class TripleLetterSquare(Square):
    def __init__(self):
        super(TripleLetterSquare, self).__init__(3, 1, "tripleLetter")

class DoubleWordSquare(Square):
    def __init__(self):
        super(DoubleWordSquare, self).__init__(1, 2, "doubleWord")

class TripleWordSquare(Square):
    def __init__(self):
        super(TripleWordSquare, self).__init__(1, 3, "tripleWord")

class StartSquare(Square):
    def __init__(self):
        super(StartSquare, self).__init__(1, 2, "start")
