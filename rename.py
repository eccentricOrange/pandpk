from argparse import ArgumentParser
from argparse import Namespace as ArgNamespace
from pathlib import Path
from re import compile as re_compile
from re import findall, split
from sys import argv
from typing import Generator

from colorama import Fore, Style
from roman import fromRoman

DATE_REGEX = re_compile(r'\d{1,2}[-_]\d{1,2}[-_]\d{4}')


def define_and_read_args(arguments: list[str]) -> ArgNamespace:

    main_parser = ArgumentParser(
        prog='rename',
        description='Rename files in a directory',
    )

    main_parser.add_argument(
        '-d',
        '--directory',
        type=str,
        help='Directory to rename files in',
        required=False,
        default='.'
    )

    main_parser.add_argument(
        '-g',
        '--glob',
        type=str,
        help='Glob expression to match files to rename',
        required=False,
        default='*'
    )

    return main_parser.parse_args(arguments)


def rename(files: Generator[Path, None, None], directory: Path) -> None:

    for file in files:
        print(f"\n{file.stem}")

        try:
            date, month, year = str(DATE_REGEX.findall(file.stem)[0]).split('-')
            lesson_name = DATE_REGEX.split(file.stem)[1].strip('-_')
            reference_material = findall(r'Reference_Material_[IVX]*', file.stem)[0]
            reference_material_roman = split(r'Reference_Material_', reference_material)[1]

        except Exception:
            print(f"{Fore.RED}{Style.BRIGHT}[Wrong format]{Style.RESET_ALL}")

        else:
            reference_material_count = fromRoman(reference_material_roman)
            new_file_name = f'{year}-{month}-{date}-{lesson_name}-{reference_material_count}{file.suffix}'
            new_file_name = new_file_name.replace('_', '-').lower()

            file.rename(directory / new_file_name)

            print(f"Renamed to {Fore.GREEN}{Style.BRIGHT}{new_file_name}{Style.RESET_ALL}")


def main(arguments: list[str]) -> None:
    parsed_namespace = define_and_read_args(arguments)
    directory = Path(parsed_namespace.directory)
    rename(directory.glob(parsed_namespace.glob), directory)


if __name__ == '__main__':
    main(argv[1:])
