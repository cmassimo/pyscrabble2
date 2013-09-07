//A dumping ground for random functions
module Scrabble.Core.Helper

open System

let ToKey (pair : Collections.Generic.KeyValuePair<_, _>) =
    pair.Key

let ToValue (pair : Collections.Generic.KeyValuePair<_, _>) =
    pair.Value

let nTimes n f = 
    let mutable i = n
    while i > 0 do
        f()
        i <- i - 1

let subsets xs = 
    List.foldBack (fun x rest -> rest @ List.map (fun ys -> x::ys) rest) xs [[]]

let rec distribute e = function
    | [] -> [[e]]
    | x::xs' as xs -> (e::xs)::[for xs in distribute e xs' -> x::xs]

let rec permute = function
    | [] -> [[]]
    | e::xs -> List.collect (distribute e) (permute xs)
