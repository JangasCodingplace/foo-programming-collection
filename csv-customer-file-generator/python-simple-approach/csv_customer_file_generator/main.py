import logging
import argparse
from pathlib import Path
from dataclasses import dataclass
from random import randint
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_fmt = logging.Formatter("%(name)s %(asctime)s %(levelname)-8s %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_fmt)
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_DIR / "generator.log")
file_handler.setFormatter(log_fmt)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


@dataclass(frozen=True)
class CommandLineArgs:
    target: Path
    article_count: int
    customer_count: int
    min_date: datetime
    max_date: datetime
    row_count: int

    def __str__(self):
        return ", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])


@dataclass
class CustomerOrder:
    customer_id: int
    article_id: int
    order_id: int
    timestamp: int


def parse_command_line_args() -> CommandLineArgs:
    parser = argparse.ArgumentParser(
        description='CSV Customer File Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--target',
        type=str,
        help='Target directory for generated csv file',
        default=str(BASE_DIR / "output"),
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
    logger.debug("Script Started")
    command_line_args = parse_command_line_args()
    logger.debug(f"Settings: {command_line_args}")
    start_time_generator_init = datetime.now()
    generator = Generator(
        article_count=command_line_args.article_count,
        customer_count=command_line_args.customer_count,
        min_date=command_line_args.min_date,
        max_date=command_line_args.max_date,
    )
    end_time_generator_init = datetime.now()
    d_t_generator_init = (end_time_generator_init - start_time_generator_init).microseconds
    logger.debug(f"Generator init took {d_t_generator_init}ms")

    start_time_row_generator = datetime.now()
    rows = generator.generate_rows(command_line_args.row_count)
    end_time_row_generator = datetime.now()
    d_t_row_generator = (end_time_row_generator - start_time_row_generator).microseconds
    logger.debug(f"Generating rows took {d_t_row_generator}ms")

    start_time_file_bump = datetime.now()
    generator.bump_to_file(command_line_args.target, rows)
    end_time_file_bump = datetime.now()
    d_t_file_bump = (end_time_file_bump - start_time_file_bump).microseconds
    logger.debug(f"File Bump took {d_t_file_bump}ms")


if __name__ == "__main__":
    main()
