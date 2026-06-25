package com.pp.laborator
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

sealed class HashMapOp (public var hashMap:HashMap<Int,Int>){
    fun sum():Int
    {
        var sum:Int=0;
        hashMap.forEach{
            sum+=it.value
        }
        return sum
    }

    fun mul():Int
    {
        var mul:Int=1
        hashMap.forEach{
            mul*=it.value
        }
        return mul
    }

}

class RunOp(hashmap: HashMap<Int, Int>, public var option:Int):HashMapOp(hashmap)
{
    var rezultat:Int=0
    var mutex=Mutex()
    var counterContex= newSingleThreadContext("CounterContext")
    suspend fun runOperation()= runBlocking {
        withContext(counterContex)
        {
            mutex.withLock{
                if(option==1)
                    rezultat=sum()
                else if(option==2)
                    rezultat=mul()
            }
        }
    }

}
