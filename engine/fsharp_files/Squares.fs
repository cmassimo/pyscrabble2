namespace Scrabble.Core.Squares

[<AbstractClass>]
type Square(letterMult:int, wordMult:int, gradient:string) = 
    let mutable tile = null
    member this.LetterMultiplier with get() = if tile = null then letterMult else 1
    member this.WordMultiplier with get() = if tile = null then wordMult else 1
    member this.Tile with get() = tile and set t = tile <- t
    member this.IsEmpty with get() = tile = null
    member this.Gradient with get() = gradient

type NormalSquare() = 
    inherit Square(1, 1, "FFFFFFFF")

type DoubleLetterSquare() =
    inherit Square(2, 1, "FF9696FF")

type TripleLetterSquare() =
    inherit Square(3, 1, "FF0000FE")

type DoubleWordSquare() =
    inherit Square(1, 2, "FFFF3C3C")

type StartSquare() =
    inherit DoubleWordSquare()

type TripleWordSquare() =
    inherit Square(1, 3, "FFFF0000")