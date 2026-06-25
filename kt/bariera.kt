import java.util.*
class Bariera (private val nrMaxFire: Int){
    private var lock = java.lang.Object()
    @Volatile private var nrFire: Int=0

    fun await()= synchronized(lock)
    {
        nrFire++

        while(nrFire<nrMaxFire)
        {
            Thread.sleep(1000)
            lock.wait()
        }

        lock.notifyAll()
    }

}
