from argparse import ArgumentParser
from argparse import Namespace as ArgNamespace
from pathlib import Path
from re import compile as re_compile
from re import findall, split
from sys import argv
from typing import Generator
from datetime import datetime

from colorama import Fore, Style
from roman import fromRoman


OLD_REGEX = re_compile(r'.*Reference_Material_(?P<reference_number>[IVX]*)_(?P<day>\d{2})[-_](?P<month>\d{2})[-_](?P<year>\d{4})_(?P<number>\d{0,2})_(?P<topic>[\w_]*)')

NEW_REGEX = re_compile(r'.*ReferenceMaterial(?P<reference_number>[IVX]*)_(?P<day_name>\w{3})(?P<month>\w{3})(?P<day>\d{2})[\d_]*IST(?P<year>\d{4})_(?P<topic>[\w-]*)')


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

    main_parser.add_argument(
        '-l',
        '--legacy',
        action='store_true',
        help='Use legacy regex, for Fall Semester 2022-23',
        required=False,
        default=False
    )

    return main_parser.parse_args(arguments)


def convert_date(day_name: str, month: str, year: str) -> str:
    return datetime.strptime(
        f'{day_name} {month} {year}',
        '%a %b %Y'
    ).strftime('%Y-%m-%d')

def new_convert(
        day_name: str,
        month: str,
        year: str,
        reference_number: str,
        topic: str,
        number: str
) -> str:
    formatted_topic = topic.replace('_', '-').replace(' ', '-').lower()

    return f'{convert_date(day_name, month, year)}-{formatted_topic}-{fromRoman(reference_number)}-{number}'


def old_convert(
        day: str,
        month: str,
        year: str,
        reference_number: str,
        topic: str,
        number: str
) -> str:
    formatted_topic = topic.replace('_', '-').replace(' ', '-').lower()

    return f'{year}-{month}-{day}-{formatted_topic}-{fromRoman(reference_number)}-{number}'


def rename(files: Generator[Path, None, None], directory: Path, legacy: bool) -> None:

    for file in files:
        print(f"\n{file.stem}")

        try:
            if legacy:
                if extracted_data := OLD_REGEX.match(file.stem):
                    new_file_name = old_convert(**extracted_data.groupdict())

                else:
                    raise ValueError('No match')
                
            else:
                if extracted_data := NEW_REGEX.match(file.stem):
                    new_file_name = new_convert(**extracted_data.groupdict())

                else:
                    raise ValueError('No match')

        except Exception:
            print(f"{Fore.RED}{Style.BRIGHT}[Wrong format]{Style.RESET_ALL}")

        else:
            file.rename(directory / f"{new_file_name}{file.suffix}")
            
            print(f"Renamed to {Fore.GREEN}{Style.BRIGHT}[{new_file_name}]{Style.RESET_ALL}")


def main(arguments: list[str]) -> None:
    parsed_namespace = define_and_read_args(arguments)
    directory = Path(parsed_namespace.directory)
    rename(
        directory.glob(parsed_namespace.glob),
        directory,
        parsed_namespace.legacy
    )

if __name__ == '__main__':
    main(argv[1:])