val makeMultiplier = { x: Int ->
    { y: Int -> x * y }
}

val add: (Int) -> (Int) -> Int = { x ->
    { y -> x + y }
}

fun operate(x: Int, y: Int, op: (Int, Int) -> Int): Int {
    return op(x, y)
}


fun main() {
    val result = operate(3, 4) { a, b -> a * b }
    println(result) 

    val numbers = listOf(4, 10, 7, 8)
    val result2 = numbers
        .chunked(2) 
        .map { it[0] * it[1] }
        .sum()

    println(result2)

    val a = listOf(1, 2, 3)
    val b = listOf("a", "b", "c")
    val result = a.zip(b) // [(1, a), (2, b), (3,c)]
    listOf(1, 2, 3, 4).zipWithNext() // [(1,2), (2,3), (3,4)] 
}
