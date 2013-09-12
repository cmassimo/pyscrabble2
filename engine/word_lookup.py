from config import WORDLIST_PATH
from combination_generator import CombinationGenerator

class WordLookup(object):
    def __init__(self):
        self.valid_words = set()
        self.official_words = dict()

        with open(WORDLIST_PATH, 'r') as f:

            for word in f.readlines():
                stripped = word.rstrip().lower()

                if len(stripped) > 1:
                    self.valid_words.add(stripped)

                    alphabetized = ''.join(sorted(stripped))

                    self.official_words.setdefault(alphabetized, []).append(stripped)

    def is_valid_word(self, word):
        return word and (word.lower() in self.valid_words)

    def find_all_words(self, letters, min_length =2, max_length =15):
        return self.find(letters, min_length, max_length)

    def find_words_using(self, letters, use_char_at, min_length =2, max_length =15):
        return self.find(letters, min_length, max_length, use_char_at)

    def find(self, letters, min_length, max_length, use_char_at =-1):
        length = len(letters)

        if use_char_at == -1:
            use_char = use_char_at
            char_adjusted_length = length
            chars = list(letters)
        else:
            use_char = use_char_at
            char_adjusted_length = length - 1
            tmp = list(letters)
            tmp.pop(use_char)
            chars = tmp

        maxlength = min(char_adjusted_length, max_length)
        valid_words = set()

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

                results = self.official_words.get(possible.lower())

                if results:
                    valid_words.update(results)

        if use_char == -1:
            return list(valid_words)
        else:
            x = self.official_words.get(letters[use_char])
            if x:
               return x + list(valid_words)
            else:
                return list(valid_words)
