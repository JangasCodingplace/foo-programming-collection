import argparse
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class CommandLineArgs:
    target: Path


def parse_command_line_args() -> CommandLineArgs:
    parser = argparse.ArgumentParser(description='CSV Customer File Generator')
    parser.add_argument(
        '--target',
        type=str,
        help='Target directory for generated csv file',
        default=str(Path(__file__).parent / "output")
    )

    args = parser.parse_args()
    return CommandLineArgs(
        target=Path(args.target)
    )


def main():
    command_line_args = parse_command_line_args()
    print()


if __name__ == "__main__":
    main()
