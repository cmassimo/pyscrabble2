from config import GameConfig
from combination_generator import CombinationGenerator

from copy import deepcopy

class WordLookup(object):
    # def __init__(self):
    valid_words = set()
    official_words = dict()

    with open(GameConfig.wordlist_path, 'r') as f:

        for word in f.readlines():
            stripped = word.rstrip().lower()

            if len(stripped) > 1:
                valid_words.add(stripped)

                alphabetized = ''.join(sorted(stripped))

                official_words.setdefault(alphabetized, []).append(stripped)

    def is_valid_word(self, word):
        return word and (word.lower() in self.valid_words)

    def find_all_words(self, letters, min_length =2, max_length =15):
        return self.find(letters, min_length, max_length)

    def find_words_using(self, letters, use_char_at, min_length =1, max_length =15):
        return self.find(letters, min_length, max_length, use_char_at)

    def find(self, ltrs, min_length, max_length, use_char_at =-1):
        length = len(ltrs)
        letters = [deepcopy(l) for l in ltrs]


        if use_char_at == -1:
            use_char = use_char_at
            char_adjusted_length = length
            chars = letters
        else:
            use_char = use_char_at
            char_adjusted_length = length - 1
            chars = [letters[i] for i in range(0, len(letters)) if i != use_char]

        maxlength = min(char_adjusted_length, max_length)
        validwords = set()

        for i in range(min_length, maxlength+1):
            generator = CombinationGenerator(char_adjusted_length, i)

            while generator.has_next():
                indices = generator.get_next()

                word = []

                for j in range(0, len(indices)):
                    word.append(chars[indices[j]])
                
                if use_char != -1:
                    word.append(letters[use_char])

                word.sort()
                possible = ''.join(word)

                results = deepcopy(self.official_words.get(possible.lower()))

                if results:
                    validwords.update(results)

        if use_char == -1:
            return list(validwords)
        else:
            x = deepcopy(self.official_words.get(letters[use_char]))
            if x:
               return x + list(validwords)
            else:
                return list(validwords)
