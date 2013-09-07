module Scrabble.Core.HillClimbingAI

open Scrabble.Core.Config
open Scrabble.Core.Squares
open Scrabble.Core.Types
open Scrabble.WordLookup
open Scrabble.Core.AI

// Provides the same as functionality as the move generator, but implements a hill-climbing technique.
// That is, discontinues the search when a local maximum is found and returns that move.
// A future implementation could take another parameter which would signify a number of random restarts
// that could be used - when a local maximum is found, choose another tile at random and perform another
// hill climb and repeat x times.  At the end, the best of the local maxima would be returned.
type HillClimbingMoveGenerator(lookup:WordLookup, ?restartTries:int) = 
    let mutable restarts = defaultArg restartTries 1

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

        let mutable bestScore = 0.0
        let mutable bestMove = Unchecked.defaultof<Move>
        let rand = System.Random()
        
        while restarts > 0 do
            let mutable stop = false
            let mutable currScore = 0.0
            let mutable currMove = Unchecked.defaultof<Move>
            let randomPossibilities = (possibleWords |> Seq.sortBy(fun x -> rand.Next())) |> Seq.toList
            if randomPossibilities.Length = 0 then
                stop <- true
                restarts <- restarts - 1

            for o in orientations do
                for word in randomPossibilities do
                    for start in PossibleStarts(word, o) do
                        if not(stop) then
                            let move = Move(Map.ofSeq 
                                                [| for i in 0 .. word.Length-1 do
                                                    yield (start.Next(o, i), new Tile(word.ToUpper().[i]))
                                                |])
                            let score = utilityMapper(tilesInHand, move.Letters)
                            if score > currScore then
                                currScore <- score
                                currMove <- move
                            else
                                stop <- true
                                restarts <- restarts - 1
                                if currScore > bestScore then
                                    bestScore <- currScore
                                    bestMove <- currMove
        
        if bestScore > 0.0 then
            PlaceMove(bestMove.Letters) :> Turn
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

        let mutable bestScore = 0.0
        let mutable bestMove:Move = Unchecked.defaultof<Move> //hack?
        let rand = System.Random()
        
        while restarts > 0 do
            let mutable stop = false
            let mutable currScore = 0.0
            let mutable currMove = Unchecked.defaultof<Move>
            let randomSquares = (b.OccupiedSquares() |> Seq.sortBy(fun x -> rand.Next())) |> Seq.toList
            let lastSquare = randomSquares |> List.rev |> List.head

            for coordinate in randomSquares do
                if not(stop) then 
                    let tile = b.Get(coordinate.Key).Tile :?> Tile
                    let possibleWords = lookup.FindWordsUsing(tile.Letter :: letters, 0)
                    if possibleWords.Length = 0 then
                        if coordinate = lastSquare then
                            stop <- true
                            restarts <- restarts - 1
                    else
                        let lastWord = possibleWords |> List.rev |> List.head
                        // this is some really terrible code. I can't believe I wrote it.
                        // but there's no break, no goto.. so the only other option would be to perform a 
                        // bunch of unnecessary work after the local maximum is found, which defeats the whole
                        // purpose of hill climbing in the first place. 
        
                        // That is being done in the first move, just to keep that code cleaner and since the number
                        // of possiblities is insignificantly small
                        for orient in orientations do
                            if not(stop) then 
                                for word in possibleWords do
                                    if not(stop) then 
                                        let moves = ValidMoves(coordinate.Key, word, orient, b)
                                        if (moves |> Seq.toList).Length = 0 && coordinate = lastSquare && word = lastWord && orient = Orientation.Horizontal then
                                            restarts <- restarts - 1
                                            stop <- true
                                        for move in moves do
                                            if not(stop) then
                                                let score = utilityMapper(tilesInHand, move.Letters)
                                                if score > currScore then
                                                    currScore <- score
                                                    currMove <- move
                                                else
                                                    stop <- true
                                                    restarts <- restarts - 1
                                                    if currScore > bestScore then
                                                        bestScore <- currScore
                                                        bestMove <- currMove
        
        if bestScore > 0.0 then
            PlaceMove(bestMove.Letters) :> Turn
        else
            Pass() :> Turn
            


    /// doesn't care if this is the first move or any subsequent move
    /// Returns the best move as defined by the move with the highest score based on 
    /// the passed in utility mapper 
    member this.Think(tilesInHand, utilityMapper) = 
            (this :> IIntelligenceProvider).Think(tilesInHand, utilityMapper)

    interface IIntelligenceProvider with
        member this.Think (tilesInHand, utilityMapper): Turn = 
            restarts <- defaultArg restartTries 1
            let b = Game.Instance.PlayingBoard
            match b.OccupiedSquares().IsEmpty with
                true -> CalculateFirstMove(tilesInHand, utilityMapper)
                | false -> CalculateBestMove(tilesInHand, b, utilityMapper)