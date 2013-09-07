module Scrabble.Core.AI

open Scrabble.Core.Config
open Scrabble.Core.Squares
open Scrabble.Core.Types
open Scrabble.WordLookup

type MoveGenerator(lookup:WordLookup) =

    // first word of the game must include (7,7)
    let PossibleStarts(word:string, o:Orientation): Coordinate list =
        let highestStart:int = max 0 (7 - word.Length + 1)

        [for i in highestStart .. 7 do
            match o with
                Orientation.Vertical -> yield new Coordinate(7, i)
                | _ -> yield new Coordinate(i, 7)]

    // simple case - this is the first move, so there is nothing on the board.
    // we just choose the best move based on the score given in the utility function
    // as long as the center tile is included
    let CalculateFirstMove(tilesInHand: TileList, utilityMapper): Turn = 
        let possibleWords = lookup.FindAllWords(tilesInHand |> Seq.map (fun w -> w.Letter) |> Seq.toList)
        let orientations:seq<Orientation> = Seq.cast(System.Enum.GetValues(typeof<Orientation>))

        let moves:Move list = 
            [ for o in orientations do
                   for word in possibleWords do
                       for start in PossibleStarts(word, o) do
                           yield Move(
                                Map.ofSeq 
                                    [| for i in 0 .. word.Length-1 do
                                          yield (start.Next(o, i), new Tile(word.ToUpper().[i]))
                                    |])
            ]
        if (moves |> Seq.filter(fun x -> utilityMapper(tilesInHand, x.Letters) > 0.0) |> Seq.toList).Length  > 0 then
            let move = moves |> Seq.maxBy (fun m -> utilityMapper(tilesInHand, m.Letters))
            PlaceMove(move.Letters) :> Turn
        else
            Pass() :> Turn



    // returns a list of starting coordinates that would result in a valid play of the given
    // word at the given tile for the given orientation.
    let ValidMoves(c:Coordinate, word:string, o:Orientation, b:Board): Move list = 
        //first generate all possible
        let letter = (b.Get(c).Tile :?> Tile).Letter
        
        // these are valid on a clear board 
        // (if there are no tiles in the way and if no invalid words are created as a side effect)
        let uncheckedStarts = 
            [| for i in 0 .. word.Length - 1 do
                if word.ToUpper().[i] = letter then
                    match o with
                        | Orientation.Horizontal -> if (c.X - i) >= 0 && (c.X + word.Length - i) <= 14 then 
                                                        yield Coordinate(c.X - i, c.Y)
                        | _ -> if (c.Y - i) >= 0 && (c.Y + word.Length - i) <= 14 then 
                                    yield Coordinate(c.X, c.Y - i) |]
        
        [for start in uncheckedStarts do
            let map = Map.ofSeq 
                        [| for i in 0 .. word.Length-1 do
                                let coord = start.Next(o, i)
                                if not(b.HasTile(coord)) then //don't include tiles already on the board in the move
                                    yield (coord, new Tile(word.ToUpper().[i]))
                        |]
            if map.Count > 0 then
                let move = Move(map)
                if move.IsValid then yield move]

    //for each occupied square, find all possible words using that tile and the letters in hand.
    // then find all ways to play on that tile, and check if each is valid.
    // from all valid moves, take the max score
    let CalculateBestMove(tilesInHand: TileList, b:Board, utilityMapper): Turn = 
        let letters = tilesInHand |> Seq.map (fun w -> w.Letter) |> Seq.toList
        let orientations:seq<Orientation> = Seq.cast(System.Enum.GetValues(typeof<Orientation>))

        let moves = 
            [| for coordinate in b.OccupiedSquares() do
                let tile = b.Get(coordinate.Key).Tile :?> Tile
                let possibleWords = lookup.FindWordsUsing(tile.Letter :: letters, 0)

                for orient in orientations do
                    for word in possibleWords do
                        for move in ValidMoves(coordinate.Key, word, orient, b) do
                            yield move
            |]  
        
        match (moves |> Seq.filter(fun x -> utilityMapper(tilesInHand, x.Letters) > 0.0) |> Seq.toList).Length with
            | 0 -> Pass() :> Turn
            | _ -> let move = moves |> Seq.maxBy (fun m -> utilityMapper(tilesInHand, m.Letters))
                   PlaceMove(move.Letters) :> Turn
            


    /// doesn't care if this is the first move or any subsequent move
    /// Returns the best move as defined by the move with the highest score based on 
    /// the passed in utility mapper 
    member this.Think(tilesInHand, utilityMapper) = 
            (this :> IIntelligenceProvider).Think(tilesInHand, utilityMapper)

    interface IIntelligenceProvider with
        member this.Think (tilesInHand, utilityMapper): Turn = 
            let b = Game.Instance.PlayingBoard
            match b.OccupiedSquares().IsEmpty with
                true -> CalculateFirstMove(tilesInHand, utilityMapper)
                | false -> CalculateBestMove(tilesInHand, b, utilityMapper)