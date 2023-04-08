import java.time.LocalDate

object Main {
  def main(args: Array[String]): Unit = {
    val articles = Generator.getArticles(100)
    val customers = Generator.getCustomers(1000)
    val minDate = LocalDate.of(2022, 1,1)
    val maxDate = LocalDate.of(2023, 1,1)
    val dates = Generator.getDates(minDate, maxDate)
  }
}
