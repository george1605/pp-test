import kotlinx.coroutines.*

fun main() = runBlocking {
    launch(Dispatchers.IO) { 
        println("IO: ${Thread.currentThread().name}")
    }
    launch(Dispatchers.Default) { 
        println("Default: ${Thread.currentThread().name}")
    }
    launch(Dispatchers.Main) { 
        println("Main: ${Thread.currentThread().name}")
    }
}
