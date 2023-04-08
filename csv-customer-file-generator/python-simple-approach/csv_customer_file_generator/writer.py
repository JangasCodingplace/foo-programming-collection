from pathlib import Path
from models import CustomerOrder


class Writer:
    @staticmethod
    def csv_file_writer(dir_path: Path, rows: list[CustomerOrder]):
        dir_path.mkdir(exist_ok=True)
        with open(dir_path / "customer-orders.csv", "w") as f:
            header = "CustomerId,ArticleId,OrderId,Timestamp"
            str_rows = "\n".join([",".join(list(map(str, row.__dict__.values()))) for row in rows])
            f.write(f"{header}\n{str_rows}")
