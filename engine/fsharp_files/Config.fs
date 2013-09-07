namespace Scrabble.Core.Config

open System
open Scrabble.Core
open Scrabble.Core.Squares

type Orientation =
    | Vertical = 0
    | Horizontal = 1

/// A simple, sortable class for an (X, Y) coordinate pair for the game board.
type Coordinate(x:int, y:int) = 
    member this.X with get() = x
    member this.Y with get() = y
    member this.Print() = 
        printfn "(%i, %i)" this.X this.Y
    member this.Neighbors() =
        [ 
            if Coordinate.ValidXY(this.X - 1) then
                yield Coordinate(this.X - 1, this.Y)

            if Coordinate.ValidXY(this.Y - 1) then
                yield Coordinate(this.X, this.Y - 1)

            if Coordinate.ValidXY(this.X + 1) then
                yield Coordinate(this.X + 1, this.Y)

            if Coordinate.ValidXY(this.Y + 1) then
                yield Coordinate(this.X, this.Y + 1)
        ]
    /// Well this sucks, apparently types aren't nullable. This is shitty design to have objects be in invalid states, but I'm not sure how to rework this...
    member this.IsValid() =
        Coordinate.ValidXY(this.X) && Coordinate.ValidXY(this.Y)
    member this.Next(o:Orientation) = 
        this.Next(o,1)
    member this.Next(o:Orientation, offset:int) = 
        match o with
        | Orientation.Horizontal -> Coordinate(this.X + offset, this.Y)
        | _ -> Coordinate(this.X, this.Y + offset)
    member this.Prev(o:Orientation) = 
        match o with
        | Orientation.Horizontal -> Coordinate(this.X - 1, this.Y)
        | _ -> Coordinate(this.X, this.Y - 1)

    //Static members
    static member Between(c0:Coordinate, c1:Coordinate) =
        let coords = Seq.ofList [ c0; c1 ]
        let first = coords |> Seq.min
        let last = coords |> Seq.max
        if first.X = last.X then
            [| first.Y .. last.Y |] |> Seq.map (fun y -> Coordinate(first.X, y)) |> Seq.toArray
        else if first.Y = last.Y then
            [| first.X .. last.X |] |> Seq.map (fun x -> Coordinate(x, first.Y)) |> Seq.toArray
        else
            raise (UnsupportedCoordinateException("Coordinates are not on the same axis."))
    static member ValidXY(i:int) = 
        i >= 0 && i < ScrabbleConfig.BoardLength

    //IComparable interface
    interface IComparable with  
         member this.CompareTo(o) = 
            let other = o :?> Coordinate
            let compareX = this.X.CompareTo(other.X)
            if compareX = 0 then
                this.Y.CompareTo(other.Y)
            else
                compareX
    override this.GetHashCode() =
        this.X.GetHashCode() + this.Y.GetHashCode()
    override this.Equals(o) =
        match o with
        | :? Coordinate as other -> this.X = other.X && this.Y = other.Y
        | _ -> false

and ScrabbleConfig() = 
    //I'm intentionally leaving out the 2 blank tiles for now.
    static member LetterQuantity : Map<char, int> = Map.ofList [ ('A', 9) ; ('B', 2) ; ('C', 2) ; ('D', 4) ; ('E', 12) ; ('F', 2) ; ('G', 3) ; ('H', 2) ; ('I', 9) ; ('J', 1) ; ('K', 1) ; ('L', 4) ; ('M', 2) ; ('N', 6) ; ('O', 8) ; ('P', 2) ; ('Q', 1) ; ('R', 6) ; ('S', 4) ; ('T', 6) ; ('U', 4) ; ('V', 2) ; ('W', 2) ; ('X', 1) ; ('Y', 2) ; ('Z', 1) ]
    static member MaxTiles : int = 7
    static member AllTilesBonus : int = 50
    static member BoardLength : int = 15
    static member StartCoordinate with get() = Coordinate(7, 7)
    static member BoardLayout(c:Coordinate) =  // I hope I didn't fuck this up. This is left handed coordinates btw. Top left is (0, 0)
        match c.X, c.Y with
        | (0, 0) | (0, 7) | (0, 14) | (7, 0) | (14, 0) | (7, 14) | (14, 7) | (14, 14) -> TripleWordSquare() :> Square //wow I really have to "downcast" this to its base type? freakin lame.

        | (5, 1) | (9, 1) | (1, 5) | (5, 5) | (9, 5) | (13, 5) 
        | (1, 9) | (5, 9) | (9, 9) | (13, 9) | (5, 13) | (9, 13)  -> TripleLetterSquare() :> Square

        | (1, 1) | (2, 2) | (3, 3) | (4, 4) | (10, 4) | (11, 3) | (12, 2) | (13, 1) 
        | (1, 13) | (2, 12) | (3, 11) | (4, 10) | (13, 13) | (10, 10) | (12, 12) | (11, 11) -> DoubleWordSquare() :> Square

        | (3, 0) | (11, 0) | (6, 2) | (8, 2) | (0, 3) | (7, 3) | (14, 3) | (2, 6) | (6, 6) | (8, 6) | (12, 6) | (3, 7) | (11, 7)
        | (2, 8) | (6, 8) | (8, 8) | (12, 8) | (0, 11) | (7, 11) | (14, 11) | (6, 12) | (8, 12) | (3, 14) | (11, 14) -> DoubleLetterSquare() :> Square

        | (7, 7) -> StartSquare() :> Square

        | _ -> NormalSquare() :> Square