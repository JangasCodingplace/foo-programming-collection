import models.CustomerOrder

import java.time.LocalDate
import java.util.UUID


object Generator {
  def getArticles(count: Int): List[String] =
    (for (_ <- 1 to count) yield UUID.randomUUID().toString).toList
  def getCustomers(count: Int): List[String] =
    (for (_ <- 1 to count) yield UUID.randomUUID().toString).toList
  def getDates(minDate: LocalDate, maxDate: LocalDate): List[LocalDate] =
    (for (i <- 1 to (maxDate.toEpochDay - minDate.toEpochDay).toInt)
      yield minDate.plusDays(i)).toList

  def generateCustomerOrders(): List[CustomerOrder] = ???
}
