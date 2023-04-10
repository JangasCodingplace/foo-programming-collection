package models

case class CustomerOrder(customerId: String, articleId: String, orderId: Int, timestamp: Int) {
  override def toString: String = s"$customerId,$articleId,$orderId,$timestamp"
}
