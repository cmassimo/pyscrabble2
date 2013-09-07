namespace Scrabble.WordLookup

open System
open System.IO
open System.Text
open System.Collections.Generic
open Combinatorics

type WordLookup() = 
    static let ValidWords = new HashSet<string>()
    static let mutable OfficialWords:Map<string, string list> = Map.empty

    static do 
        File.ReadAllLines(@"..\..\..\twl.txt")
            |> Seq.map(fun w -> w.ToLower())
            |> Seq.iter(fun w -> 
                            ValidWords.Add w |> ignore
                            let alphabetized = new string (w |> Seq.sort |> Seq.toArray)

                            match OfficialWords.TryFind alphabetized with
                                // this is terrible, but you can't modify an existing member in the map
                                //pretty sure there has to be a functional way to build this map but it's evading me...
                                | Some x -> OfficialWords <- OfficialWords.Remove(alphabetized); 
                                            OfficialWords <- OfficialWords.Add(alphabetized, w :: x)
                                | None -> OfficialWords <- OfficialWords.Add(alphabetized, w::[])
                        )

    
    member this.IsValidWord (word: string): bool = 
        if String.IsNullOrEmpty word then false else ValidWords.Contains (word.ToLower())

    member this.FindAllWords (letters: char list, ?minLength: int, ?maxLength: int): string list = 
        this.Find(letters, defaultArg minLength 2, defaultArg maxLength 15)

    member this.FindWordsUsing (letters: char list, useCharAt: int, ?minLength: int, ?maxLength: int): string list = 
        this.Find(letters, defaultArg minLength 2, defaultArg maxLength 15, useCharAt)

    /// shouldn't really be a member, but you can't have optional parameters on private methods
    /// call into FindAllWords or FindwordsUsing instead - both call this
    member this.Find (letters: char list, minLength: int, maxLength: int, ?useCharAt: int): string list = 
        let useChar = defaultArg useCharAt -1
        let length = Seq.length letters
        let charAdjustedLength = match useChar with | -1 -> length | _ -> length - 1
        let max = min charAdjustedLength maxLength

        let chars = match useChar with
                        | -1 -> letters |> Seq.toArray
                        | _ -> letters // a lot of code to remove an item from a list...
                                |> List.mapi (fun index element -> (index <> useChar, element)) 
                                |> List.filter fst 
                                |> List.map snd 
                                |> Seq.toArray

        let validWords =
            [ for i in minLength .. max do
                     let generator = new CombinationGenerator(charAdjustedLength, i)
                     while generator.HasNext do
                         let indices = generator.GetNext()
                         let word = new string([| for j in 0 .. indices.Length - 1 do 
                                                    yield chars.[indices.[j]] 
                                                  match useChar with
                                                      | -1 -> ()
                                                      | _ -> yield letters.[useChar] |])
                         let possible = new string(word |> Seq.sort |> Seq.toArray)

                         match OfficialWords.TryFind(possible.ToLower()) with
                             | None -> ()
                             | Some x -> for item in x do yield item
             ]

        match useChar with
            | -1 -> validWords |> Seq.distinct |> Seq.toList
            | _ -> match OfficialWords.TryFind(letters.[useChar].ToString()) with
                    | None -> validWords |> Seq.distinct |> Seq.toList
                    | Some x -> x @ (validWords |> Seq.distinct |> Seq.toList)