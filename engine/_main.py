__author__ = 'jacky'

from string import letters
from engine.game import ScrabbleGame
from engine import board
from lexicon.lexicon_set import read_lexicon
from lexicon.gaddag import gaddag_from_file
# from engine import move_generator
from move_generator import MoveGenerator

game = ScrabbleGame()
columns = letters[:len(game.board[0])].upper()
# columns = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14']

# Test using the fake wordlist and bag?
TEST = False

def print_game():
    print '    ' + ' '.join(columns)
    for i, row in enumerate(game.board):
        r = []
        r.append('%2d|' % i)
        for sym in row:
            r.append(board.colors[sym] + sym + board.colors[sym])
        r.append(board.standard_color)
        print ' '.join(r)

    print '\nSCORES'
    scores = game.get_scores()
    for k, v in scores.items():
        print '%s: %d' % (k, v)

    info = game.current_player_info()

    print "\n%s's rack:" % info['name']
    print info['rack']


def start_game():
    # name = raw_input('Enter player 1 name: ')
    game.add_player('AI1')

    # name = raw_input('Enter player 2 name: ')
    game.add_player('A12')

    for player in game.players:
        player.ai = MoveGenerator();

    game.start_game()

def get_move():
    # RE_INVALID = 'INVALID MOVE CANDIDATE\n'

    # print '\nMenu:\n1. Play a move\n2. Exchange tiles\n3. Pass'
    # choice = int(raw_input('Please Choose: '))
    # print

    # if choice == 1:
        # letters = raw_input('Enter the tiles you want to play: ').upper()
        # x = int(raw_input('Row number: '))
        # y = columns.index(raw_input('Column Letter: ').upper())
        # h = raw_input('H for horizontal, V for vertical: ').upper()

        res = game.current_player().ai.think(game.current_player().rack)
        
        if res:
            letters, (x, y), h = res
            print "I'll play %s" % ''.join(letters)
            
            if game.set_candidate(letters, (x, y), h):
                if game.validate_candidate():
                    print '\n%s played %s at (%d, %d) for %d points\n' % (
                        game.current_player_info()['name'], letters, x, y, game.candidate.score)
                    game.commit_candidate()
                else:
                    print RE_INVALID
                    game.remove_candidate()
                    get_move()
            else:
                print RE_INVALID
                get_move()

        else:
            game.pass_turn()
    # elif choice == 2:
        # letters = raw_input('Enter the tiles you want to exchange: ').upper()

        # if game.exchange_tiles(letters):
            # print 'Tiles successfully exchanged'
        # else:
            # print 'Unable to exchange tiles. Try again\n'
            # get_move()
    # elif choice == 3:
        # game.pass_turn()


def main():
    if TEST:
        WORDLIST = './engine/test/wordlists/wordlist1.txt'
        game.lexicon_set = read_lexicon(WORDLIST)
        game.gaddag = gaddag_from_file(WORDLIST)
        game.bag = list('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
                        'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
                        'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')

    start_game()
    while not game.game_over:
        print_game()
        get_move()

    print '\n-----Game Over!-----'
    print 'Final scores: '
    scores = game.get_scores()
    for k, v in scores.items():
        print '%s: %d' % (k, v)

    # This doesn't care about ties, but it'll do for now.
    winner = max(scores.items(), key=scores.get)
    print 'The winner was %s with %d points!' % (winner[0], winner[1])

if __name__ == '__main__':
    main()
