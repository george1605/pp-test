// SINGLETON

object Player
{
  var inventory = mutableListOf<String>()
  // other attributes and functions here
  fun addToInventory(item: String) {
    inventory.add(item)
  }
}

Player.addHP(10)

// PROTOTYPE

interface Shape {
    fun clone(): Shape
}

class Circle(
    val radius: Int
) : Shape {

    override fun clone(): Shape {
        return Circle(radius)
    }
}

// PROXY

interface Database {
    fun query(sql: String)
}

class RealDatabase : Database {
    override fun query(sql: String) {
        println("Executing: $sql")
    }
}

class LoggingDatabaseProxy(
    private val db: Database
) : Database {

    override fun query(sql: String) {
        println("LOG: query requested")
        db.query(sql)
    }
}
