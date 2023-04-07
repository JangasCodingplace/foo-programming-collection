import argparse
from pathlib import Path
from dataclasses import dataclass
from random import randint
from datetime import datetime, timedelta


@dataclass(frozen=True)
class CommandLineArgs:
    target: Path
    article_count: int
    customer_count: int
    min_date: datetime
    max_date: datetime
    row_count: int


@dataclass
class CustomerOrder:
    customer_id: int
    article_id: int
    order_id: int
    timestamp: int


def parse_command_line_args() -> CommandLineArgs:
    parser = argparse.ArgumentParser(description='CSV Customer File Generator')
    parser.add_argument(
        '--target',
        type=str,
        help='Target directory for generated csv file',
        default=str(Path(__file__).parent / "output"),
    )
    parser.add_argument(
        '--article-count',
        type=int,
        help='Number of different article numbers which get generated',
        default=100,
    )
    parser.add_argument(
        '--customer-count',
        type=int,
        help='Number of different customers which get generated',
        default=100,
    )
    parser.add_argument(
        '--min-date',
        type=str,
        help='min-date for order generation. Should have format YYYY-mm-dd',
        default="2022-01-01",
    )
    parser.add_argument(
        '--max-date',
        type=str,
        help='max-date for order generation. Should have format YYYY-mm-dd',
        default="2023-01-01",
    )
    parser.add_argument(
        '--row-count',
        type=int,
        help='row count for order generation.',
        default=10000,
    )

    args = parser.parse_args()
    return CommandLineArgs(
        target=Path(args.target),
        article_count=args.article_count,
        customer_count=args.customer_count,
        min_date=datetime.strptime(args.min_date, "%Y-%m-%d"),
        max_date=datetime.strptime(args.max_date, "%Y-%m-%d"),
        row_count=args.row_count,
    )


class Generator:
    def __init__(
        self,
        article_count: int,
        customer_count: int,
        min_date: datetime,
        max_date: datetime
    ):
        self.articles = [i for i in range(10**5, 10**5 + article_count)]
        self.customers = [i for i in range(10 ** 3, 10 ** 3 + customer_count)]
        self.date_list = [min_date + timedelta(days=d) for d in range((max_date - min_date).days)]

    def _generate_order(self, order_id: int) -> list[CustomerOrder]:
        date = self.date_list[randint(0, len(self.date_list)-1)]
        timestamp = datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=randint(0, 23),
            minute=randint(0, 59),
            second=randint(0, 59),
        )
        customer = self.customers[randint(0, len(self.customers)-1)]
        item_count = randint(1, 20)
        articles = [self.articles[randint(0, len(self.articles)-1)] for _ in range(item_count)]
        return [
            CustomerOrder(
                customer_id=customer,
                article_id=article,
                order_id=order_id,
                timestamp=int(timestamp.timestamp()),
            ) for article in articles
        ]

    def generate_rows(self, max_row_count: int) -> list[CustomerOrder]:
        order_id = 1000
        rows = []
        while len(rows) < max_row_count:
            order = self._generate_order(order_id)
            rows += order
            order_id += 1
        return rows

    @staticmethod
    def bump_to_file(dir_path: Path, rows: list[CustomerOrder]):
        dir_path.mkdir(exist_ok=True)
        with open(dir_path / "customer-orders.csv", "w") as f:
            header = "CustomerId,ArticleId,OrderId,Timestamp"
            str_rows = "\n".join([",".join(list(map(str, row.__dict__.values()))) for row in rows])
            f.write(f"{header}\n{str_rows}")


def main():
    command_line_args = parse_command_line_args()
    generator = Generator(
        article_count=command_line_args.article_count,
        customer_count=command_line_args.customer_count,
        min_date=command_line_args.min_date,
        max_date=command_line_args.max_date,
    )
    rows = generator.generate_rows(command_line_args.row_count)
    generator.bump_to_file(command_line_args.target, rows)


if __name__ == "__main__":
    main()
