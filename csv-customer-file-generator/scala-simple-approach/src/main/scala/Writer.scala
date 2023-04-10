import models.CustomerOrder

import java.io.{BufferedWriter, File, FileWriter}
import java.nio.file.{Files, Path}

object Writer {
  def csvFileWriter(path: Path, rows: List[CustomerOrder]): Unit = {
    if (!Files.exists(path)) Files.createDirectories(path)
    val file = new File(s"${path.toString}/customer-orders.csv")
    val writer = new BufferedWriter(new FileWriter(file))
    val lines = rows.map(_.toString).mkString("\n")
    writer.write("CustomerId,ArticleId,OrderId,Timestamp\n")
    writer.write(lines)
    writer.close()
  }
}
