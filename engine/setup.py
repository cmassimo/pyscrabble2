from utility_functions import maximum_score
from support import GameState, Game, ComputerPlayer 
from move_generator import MoveGenerator

def setup_game_state(word_lookup, name1, name2):
    Game.instance = GameState(word_lookup, [
        ComputerPlayer(name1),
        ComputerPlayer(name2)
        ])

def apply_setup_values(word_lookup, player, provider_code, utility_code):
  if provider_code == 0:
    player.provider = MoveGenerator(word_lookup)
  elif provider_code == 1:
    player.provider = HillClimbingMoveGenerator(word_lookup, 15)
  elif provider_code == 2:
    player.provider = HillClimbingMoveGenerator(word_lookup, 5)
  else:
    raise Exception("Unknown utility function code.")

  if utility_code == 0:
    player.utility_function = maximum_score
  elif utility_code == 1:
    player.utility_function = smart_s_moves
  elif utility_code == 2:
    player.utility_function = save_common
  elif utility_code == 3:
    player.utility_function = only_play_7s
  elif utility_code == 4:
    player.utility_function = only_play_over5
  elif utility_code == 5:
    player.utility_function = use_bonus_squares
  else:
    raise Exception("Unknown utility function code.")

