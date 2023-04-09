import models.CustomerOrder

import java.time.{LocalDate, LocalDateTime}
import java.util.UUID
import scala.util.Random


object Generator {
  def getArticles(count: Int): List[String] =
    (for (_ <- 1 to count) yield UUID.randomUUID().toString).toList

  def getCustomers(count: Int): List[String] =
    (for (_ <- 1 to count) yield UUID.randomUUID().toString).toList

  def getDates(minDate: LocalDate, maxDate: LocalDate): List[LocalDate] =
    (for (i <- 1 to (maxDate.toEpochDay - minDate.toEpochDay).toInt)
      yield minDate.plusDays(i)).toList

  def generateCustomerOrders(maxRowCount: Int, customers: List[String], articles: List[String], dates: List[LocalDate]): List[CustomerOrder] = {
    def accOrders(orders: List[CustomerOrder], orderId: Int, maxLength: Int): List[CustomerOrder] =
      if (orders.length < maxLength) accOrders(orders ++ generateSingleOrder(orderId + 1, customers, articles, dates), orderId + 1, maxLength)
      else orders
    accOrders(List(), 0, maxRowCount)
  }

  private def generateSingleOrder(orderId: Int, customers: List[String], articles: List[String], dates: List[LocalDate]) = {
    val customer = customers(Random.nextInt(customers.length))
    val date = dates(Random.nextInt(dates.length))
    val dt = LocalDateTime.of(date.getYear, date.getMonth, date.getDayOfMonth, Random.nextInt(23), Random.nextInt(59), Random.nextInt(59))
    val timestamp = dt.atZone(java.time.ZoneOffset.UTC).toInstant.getEpochSecond.toInt
    for (_ <- 1 to Random.nextInt(20) + 1)
      yield CustomerOrder(customer, articles(Random.nextInt(articles.length)), orderId, timestamp)
  }
}
