
# default utility function, just score the move
# let MaximumScore(tiles:TileList, move) = System.Convert.ToDouble(Move(move).Score)

def maximum_score(tiles, move):
    return float(Move(move).score)
# 

# // increase 'score' of words that leave common letters left over
# // since we'll then have a better chance at a 7-letter word
# let SaveCommon(tiles:TileList, move:Map<Config.Coordinate, Tile>) = 
#     let t:Tile[] = 
#         [for tile in tiles do yield tile] |> Seq.toArray

#     let list = System.Collections.Generic.List(t)
#     for item in move do
#         list.Remove(item.Value) |> ignore

#     let mutable scale = 0

#     for tile in list do
#         match tile.Letter with
#             // per english word frequencies, these are the 7 most common letters
#             | 'E' | 'T' | 'A' | 'O' | 'I' | 'N' | 'S' -> scale <- scale + 5 //5 is arbitrary
#             | _ -> ()

#     System.Convert.ToDouble(Move(move).Score + scale)


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

# /// This move adds in the fact that by using a bonus square, you're taking away potential points
# /// from your opponents. This factors in that a Double Letter Score will on average give the opponent 1.9 points,
# /// so when the computer uses a Double Letter Score, the utility function will be + 1.9.
# let UseBonusSquares(tiles:TileList, letters: Map<Config.Coordinate, Tile>) = 
#     let avgTileScore = 1.9 //The average tile in scrabble is worth ~1.9 something
#     let avgWordScore = avgTileScore * 3.5 //We assume that the average Scrabble word has 3.5 letters in it.

#     let b = Game.Instance.PlayingBoard
#     let squares = letters |> Seq.map (fun kv -> b.Get(kv.Key))
#     let wordMult = squares |> Seq.map (fun s -> s.WordMultiplier) |> Seq.reduce (fun a b -> a * b)
    
#     let bonusList = letters |> Seq.map (fun kv -> 
#         let s = b.Get(kv.Key)
#         if s.LetterMultiplier > 1 then
#             avgTileScore * (Convert.ToDouble(s.LetterMultiplier) - 1.0)
#         else
#             0.0
#     )
#     let letterBonus = bonusList |> Seq.sum
#     let wordBonus = Convert.ToDouble(wordMult - 1) * avgWordScore

#     let move = Move(letters)
#     let baseScore = Convert.ToDouble(move.Score)
#     baseScore + letterBonus + wordBonus

# let OnlyPlayOver5(tiles:TileList, move: Map<Config.Coordinate, Tile>) = 
#     if move.Count <= 5 then 0.0 else System.Convert.ToDouble(Move(move).Score)

# let OnlyPlay7s(tiles:TileList, move: Map<Config.Coordinate, Tile>) = 
#     if move.Count < 7 then 0.0 else System.Convert.ToDouble(Move(move).Score)

# //combine two for the best of both worlds
# let SmartSMovesSaveCommon(tiles:TileList, move:Map<Config.Coordinate, Tile>) = 
#     let sMoves = SmartSMoves(tiles, move)
#     let common = SaveCommon(tiles, move)
#     max sMoves common

# let SmartSMovesSaveCommonUseBonus(tiles:TileList, move:Map<Config.Coordinate, Tile>) = 
#     let sCommon = SmartSMovesSaveCommon(tiles, move)
#     let bonus = UseBonusSquares(tiles, move)
#     max bonus sCommon