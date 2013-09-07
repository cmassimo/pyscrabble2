namespace Combinatorics

type CombinationGenerator(domain:int, choose:int) = 
    static let factorials = 
        Map.ofSeq [| (0, 1L); (1, 1L); (2, 2L); (3, 6L); (4, 24L); (5, 120L);
                     (6, 720L); (7, 5040L); (8, 40320L); (9, 362880L); (10, 3628800L);
                     (11, 39916800L); (12, 479001600L); (13, 6227020800L);
                     (14, 87178291200L); (15, 1307674368000L); |]

    let totalCombinations = factorials.[domain] / (factorials.[choose] * factorials.[domain - choose]);
    let mutable combinationsLeft = totalCombinations

    let mutable data = [| for i in 0 .. choose-1 do yield i |]

    member this.GetNext() = 
        if combinationsLeft = totalCombinations then
            combinationsLeft <- combinationsLeft - 1L
        else
            let mutable i = choose - 1
            while data.[i] = domain - choose + i do
                i <- i-1
            data.[i] <- data.[i] + 1
            for j in i + 1 .. choose - 1 do
                data.[j] <- data.[i] + j - i
            combinationsLeft <- combinationsLeft - 1L
        data

    member this.HasNext = not (combinationsLeft = 0L)