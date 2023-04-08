import argparse
from config import BASE_DIR
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class CommandLineArgs:
    target: Path
    article_count: int
    customer_count: int
    min_date: datetime
    max_date: datetime
    row_count: int
    thread_count: int

    def __str__(self):
        return ", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])


def _parse_command_line_args() -> CommandLineArgs:
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
    parser.add_argument(
        '--thread-count',
        type=int,
        help=(
            "number of threads which should be used. If number is higher than Number of CPU - 1, "
            "it will be set to CPU - 1"
        ),
        default=1,
    )

    args = parser.parse_args()
    return CommandLineArgs(
        target=Path(args.target),
        article_count=args.article_count,
        customer_count=args.customer_count,
        min_date=datetime.strptime(args.min_date, "%Y-%m-%d"),
        max_date=datetime.strptime(args.max_date, "%Y-%m-%d"),
        row_count=args.row_count,
        thread_count=args.thread_count,
    )


command_line_args = _parse_command_line_args()
