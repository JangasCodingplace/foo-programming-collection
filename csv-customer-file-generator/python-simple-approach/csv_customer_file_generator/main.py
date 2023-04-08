from datetime import datetime
from utils import get_logger
from cli import command_line_args
from generator import Generator
from writer import Writer

logger = get_logger(__name__)


def main():
    logger.debug("Script Started")
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
    Writer.csv_file_writer(command_line_args.target, rows)
    end_time_file_bump = datetime.now()
    d_t_file_bump = (end_time_file_bump - start_time_file_bump).microseconds
    logger.debug(f"File Bump took {d_t_file_bump}ms")


if __name__ == "__main__":
    main()
