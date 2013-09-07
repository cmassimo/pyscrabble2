from utility_functions import maximum_score
from types import GameState, Game, ComputerPlayer
from move_generator import MoveGenerator

def setup_game_state():
    Game.instance = GameState([
        ComputerPlayer('ASD'),
        ComputerPlayer('QWE')
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
    player.utility_function = MaximumScore
  elif utility_code == 1:
    player.utility_function = SmartSMoves
  elif utility_code == 2:
    player.utility_function = SaveCommon
  elif utility_code == 3:
    player.utility_function = OnlyPlay7s
  elif utility_code == 4:
    player.utility_function = OnlyPlayOver5
  elif utility_code == 5:
    player.utility_function = UseBonusSquares
  else:
    raise Exception("Unknown utility function code.")

