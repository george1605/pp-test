package com.pp.laborator
import java.util.concurrent.ConcurrentHashMap

val cache = ConcurrentHashMap<Int,Int>()

fun fibbonacci(n: Int) :Int = cache.getOrPut(n)
{
    when(n)
    {
        1, 0 -> 1
        else -> fibbonacci(n-1) + fibbonacci(n-2)
    }
}

fun main() {
    println(fibbonacci(6))
}
