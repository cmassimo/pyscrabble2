from engine import board, move
from word_lookup import WordLookup

class MoveGenerator(object):
    def __init__(self):
        self.lookup = WordLookup()

    def possible_starts(self, word, horizontal):
        self.highest_start = max(0, (7 - len(word) + 1))

        starts = []
        for i in range(self.highest_start, 8):
            if horizontal:
                starts.append(board.BoardPosition(None, [i, 7]))
            else:
                starts.append(board.BoardPosition(None, [7, i]))

        return starts

    def calculate_first_move(self, tiles_in_hand):
        possible_words = self.lookup.find_all_words(tiles_in_hand)

        moves = []

        horizontal = [True, False]

        print "Calculating moves"
        for o in horizontal:
            for word in possible_words:
                for start in self.possible_starts(word, o):
                    letters = []
                    start_pos = start.next_pos(o, 0)

                    for i in range(0, len(word)):
                        letters.append(word.upper()[i])

                    moves.append(move.AIMove(letters, start_pos, o))

        print "Validation moves"
        for mv in moves:
            mv.validate

        positive_scores = [mv for mv in moves if mv.score > 0]

        if positive_scores:
            to_be_played = max(positive_scores, key=lambda ps: ps.score)

            letters = [bp.letter for bp in to_be_played.positions]
            return (letters, to_be_played.positions[0].pos, to_be_played.horizontal)
            # game.set_candidate(letters, to_be_played.positions[0].pos)
            # if game.vaidate_candidate():
                # game.commit_candidate()

        else:
            return None

    def valid_moves(pos, word, horizontal, game_board):
        x, y = pos
        letter = game_board[x][y]

        unchecked_starts = []
        for i in range(0, len(word)):
            if word.upper()[i] == letter:
                if horizontal:
                    if (x - i) >= 0 and (x + len(word) - i) <= 14:
                        unchecked_starts.append([x - i, y])
                else:
                    if (y - i) >= 0 and (y + len(word) - i) <= 14:
                        unchecked_starts.append([x, y - i])

        vmoves = []
        letter_pos = []

        for start in unchecked_starts:
            for i in range(0, len(word)):
                nx, ny = board.BoardPosition(None, start).next_pos(horizontal, i)
                if game_board[nx][ny] not in board.empty_locations:
                    letter_pos.append( ([nx, ny], word.upper()[i]) )

            move = move.AIMove([lp[0] for lp in letter_pos], letter_pos[0][0], o)
            if move.validate():
                vmoves.append(move)

        return vmoves

    def calculate_best_move(tiles_in_hand):
        letters = tiles_in_hand # maybe will require extraction

        moves = []
        for coordinates in board.occupied_positions(board.game_board):
            x, y = coordinates
            possible_words = self.lookup.find_words_using(board.game_board[x][y], 0)

            for horizontal in [True, False]:
                for word in possible_words:
                    for move in self.valid_moves(coordinates, word, horizontal, board.game_board):
                        moves.append(move)

        positive_scores = [move for move in moves if move.score > 0]

        if positive_scores:
            to_be_played = max(positive_scores, key=lambda ps: ps.score)

            letters = [bp.letter for bp in to_be_played.positions]
            return (letters, to_be_played.positions[0].pos, to_be_played.horizontal)
            # game.set_candidate(letters, to_be_played.positions[0].pos)
            # if game.validate_candidate():
                # game.commit_candidate()

        else:
            return None

    def think(self, tiles_in_hand, utility_mapper =None):
        if board.occupied_positions(board.game_board):
            return self.calculate_best_move(tiles_in_hand)
        else:
            return self.calculate_first_move(tiles_in_hand)
