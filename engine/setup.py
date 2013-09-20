from utility_functions import maximum_score, save_common, only_play_7s, only_play_over5, use_bonus_squares
from support import GameState, Game, ComputerPlayer 
from move_generator import MoveGenerator
from hill_climbing_move_generator import HillClimbingMoveGenerator
from minimax import Minimax
from config import GameConfig

def setup_game_state(word_lookup, name1, name2, debug =False, web =True):
    state = GameState(word_lookup, [
        ComputerPlayer(name1, web),
        ComputerPlayer(name2, web)
        ])
    
    if debug == 'true':
      GameConfig.debug = True
      GameConfig.debug_channel = state.players[0].channel
    else:
      GameConfig.debug = False
      GameConfig.debug_channel = ""

    return state

def apply_setup_values(state, word_lookup, player, provider_code, utility_code):
  if provider_code == 0:
    player.provider = MoveGenerator(state, word_lookup)
  elif provider_code == 1:
    player.provider = HillClimbingMoveGenerator(state, word_lookup, 5)
  elif provider_code == 2:
    player.provider = HillClimbingMoveGenerator(state, word_lookup, 15)
  elif provider_code == 3:
    player.provider = Minimax(state, word_lookup)
  else:
    raise Exception("Unknown move generator code.")

  if utility_code == 0:
    player.utility_function = maximum_score
  elif utility_code == 1:
    player.utility_function = save_common
  elif utility_code == 2:
    player.utility_function = only_play_7s
  elif utility_code == 3:
    player.utility_function = only_play_over5
  elif utility_code == 4:
    player.utility_function = use_bonus_squares
  else:
    raise Exception("Unknown utility function code.")

def provider_code_mapping(provider_code):
  if provider_code == 0:
    return 'MoveGenerator'
  elif provider_code == 1:
    return 'HillClimbingMoveGenerator(15)'
  elif provider_code == 2:
    return 'HillClimbingMoveGenerator(5)'
  elif provider_code == 3:
    return 'Minimax'
  else:
    raise Exception("Unknown move generator code.")

def utility_code_mapping(utility_code):
  if utility_code == 0:
    return "maximum_score"
  elif utility_code == 1:
    return 'save_common'
  elif utility_code == 2:
    return 'only_play_7s'
  elif utility_code == 3:
    return 'only_play_over5'
  elif utility_code == 4:
    return 'use_bonus_squares'
  else:
    raise Exception("Unknown utility function code.")

