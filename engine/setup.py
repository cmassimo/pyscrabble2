from utility_functions import maximum_score
from types import GameState, Game, ComputerPlayer
from move_generator import MoveGenerator

def setup_game_state():
    Game.instance = GameState([
        ComputerPlayer('ASD'),
        ComputerPlayer('QWE')
        ])

def setup_computer():
    for player in Game.instance.computer_players:
        player.provider = MoveGenerator(Game.instance.Dictionary)
        player.utility_function = maximum_score


# let SetupGameState() = 
#     Game.Instance <- GameState([ 
#                                 ComputerPlayer("PlayerOne") :> Player 
#                                 ;ComputerPlayer("PlayerTwo") :> Player
#                                 ;ComputerPlayer("PlayerThree") :> Player 
#                                ])


# let SetupComputer() = 
#     Game.Instance.ComputerPlayers |> Seq.iter (fun c -> 
#         c.Provider <- //HillClimbingMoveGenerator(Game.Instance.Dictionary, 5) //random restart 5 times
#                         HillClimbingMoveGenerator(Game.Instance.Dictionary) 
#                         //MoveGenerator(Game.Instance.Dictionary)
#         c.UtilityFunction <- MaximumScore
#                             //SmartSMoves
#                             //SaveCommon
#                             //OnlyPlay7s
#                             //OnlyPlayOver5
#                             //UseBonusSquares
#     )

# let SetupFirstComputer() = 
#     let first = Game.Instance.ComputerPlayers |> Seq.head
    
#     first.Provider <- //HillClimbingMoveGenerator(Game.Instance.Dictionary, 5) //random restart 5 times
#                         HillClimbingMoveGenerator(Game.Instance.Dictionary) 
#                         //MoveGenerator(Game.Instance.Dictionary)
#     first.UtilityFunction <- MaximumScore
#                             //SmartSMoves
#                             //SaveCommon
#                             //OnlyPlay7s
#                             //OnlyPlayOver5
#                             //UseBonusSquares

# let SetupSecondComputer() = 
#     let second = Game.Instance.ComputerPlayers |> Seq.toList |> List.tail |> List.head
    
#     second.Provider <- //HillClimbingMoveGenerator(Game.Instance.Dictionary, 15) //random restart 5 times
#                         HillClimbingMoveGenerator(Game.Instance.Dictionary) 
#                         //MoveGenerator(Game.Instance.Dictionary)
#     second.UtilityFunction <- MaximumScore
#                             //SmartSMoves
#                             //SaveCommon
#                             //OnlyPlay7s
#                             //OnlyPlayOver5
#                             //UseBonusSquares