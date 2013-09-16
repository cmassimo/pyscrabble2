from support import Move, Game

from copy import deepcopy

def maximum_score(tiles, move, state =Game.instance):
    return float(Move(move, state).score())

def save_common(tiles, move, state =Game.instance):
    ts = deepcopy(tiles)

    # print ts

    print move
    for _, tile in move.items():
        # print tile
        # XXX a volte crasha perche` tile non e` in ts
        ts.remove(tile)

    scale = 0

    for tile in ts:
        if tile.letter in ['E', 'A', 'I', 'O', 'N']:
            scale += 5

    return float(Move(move, state).score() + scale)

# ???
# /// If an S is used, make the Move less desierable if we're not using it "properly"
# /// An S can be used to make two words at once, and if the computer is not making > 1 word with the S, then we
# /// subtract from the move's utility function.
# let SmartSMoves(tiles:TileList, letters: Map<Config.Coordinate, Tile>) = 
#     let neighbors(c:Coordinate, o:Orientation) = 
#         let n = c.Next(o)
#         let p = c.Prev(o)
#         [|
#             if n.IsValid() then
#                 yield n
#             if p.IsValid() then
#                 yield p
#         |]
#     let move = Move(letters)
#     let modifiers = letters |> Seq.filter (fun kv -> kv.Value.Letter = 'S') |> Seq.map (fun kv -> 
#         let connectors = neighbors(kv.Key, move.Orientation) |> Seq.filter (fun c -> Game.Instance.PlayingBoard.HasTile(c)) |> Seq.length
#         if connectors = 0 then
#             -5
#         else
#             0
#     )
#     let scale = modifiers |> Seq.sum
#     Convert.ToDouble(move.Score - scale)

def use_bonus_squares(tiles, letters, state =Game.instance):
    avg_tile_score = 1.9
    avg_word_score = avg_tile_score * 3.5

    board = Game.instance.playing_board
    squares = [board.get(c) for c,t in letters.items()]
    word_mult = reduce(lambda x, lm: x*lm, [s.word_multiplier for s in squares], 1)

    bonus_list = []

    for c, t in letters.items():
        s = board.get(c)
        if s.letter_multiplier > 1:
            bonus_list.append(avg_tile_score * (s.letter_multiplier - 1))

    letter_bonus = sum(bonus_list)
    word_bonus = (word_mult - 1) * avg_word_score

    move = Move(letters, state)
    base_score = move.score()

    return float(base_score + letter_bonus + word_bonus)

def only_play_over5(tiles, move, state =Game.instance):
    if len(move) > 5:
        return float(Move(move, state).score())
    else:
        return 0.0

def only_play_7s(tiles, move, state =Game.instance):
    if len(move) >= 7:
        return float(Move(move, state).score())
    else:
        return 0.0

# manca smart_s_moves().

# //combine two for the best of both worlds
# let SmartSMovesSaveCommon(tiles:TileList, move:Map<Config.Coordinate, Tile>) = 
#     let sMoves = SmartSMoves(tiles, move)
#     let common = SaveCommon(tiles, move)
#     max sMoves common

# let SmartSMovesSaveCommonUseBonus(tiles:TileList, move:Map<Config.Coordinate, Tile>) = 
#     let sCommon = SmartSMovesSaveCommon(tiles, move)
#     let bonus = UseBonusSquares(tiles, move)
#     max bonus sCommon