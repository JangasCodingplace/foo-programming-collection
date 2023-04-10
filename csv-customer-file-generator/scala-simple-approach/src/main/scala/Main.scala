import java.nio.file.Paths
import java.time.LocalDate

object Main {
  def main(args: Array[String]): Unit = {
    val startValueGenerationTs = System.currentTimeMillis()
    val articles = Generator.getArticles(100)
    val customers = Generator.getCustomers(10000)
    val minDate = LocalDate.of(2022, 1,1)
    val maxDate = LocalDate.of(2023, 1,1)
    val dates = Generator.getDates(minDate, maxDate)
    val dtValueGeneration = System.currentTimeMillis() - startValueGenerationTs
    println(s"Value Generation took $dtValueGeneration ms")

    val startOrderGeneration = System.currentTimeMillis()
    val orders = Generator.generateCustomerOrders(100000, customers, articles, dates)
    val dtOrderGeneration = System.currentTimeMillis() - startOrderGeneration
    println(s"Order Generation took $dtOrderGeneration ms")

    val startTimeWriter = System.currentTimeMillis()
    Writer.csvFileWriter(Paths.get("./output/"), orders)
    val dtWriter = System.currentTimeMillis() - startTimeWriter
    println(s"File Write took $dtWriter ms")
  }
}
