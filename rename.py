from argparse import ArgumentParser
from argparse import Namespace as ArgNamespace
from pathlib import Path
from re import compile as re_compile
from re import split, findall
from sys import argv

from roman import fromRoman
from colorama import Fore, Style


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
        required=False
    )

    main_parser.add_argument(
        '-g',
        '--glob',
        type=str,
        help='Glob expression to match files to rename',
        required=False
    )

    return main_parser.parse_args(arguments)


def get_files_to_rename(glob: str, directory: Path) -> list[Path]:
    return list(directory.glob(glob))


def rename(files: list[Path], directory: Path) -> None:

    for file in files:
        file_name = file.stem
        file_extension = file.suffix
        print(f"\n{file_name}")

        try:
            date, month, year = str(DATE_REGEX.findall(file_name)[0]).split('-')
            lesson_name = DATE_REGEX.split(file_name)[1].strip('-_')
            reference_material = findall(r'Reference_Material_[IVX]*', file_name)[0]
            reference_material_roman = split(r'Reference_Material_', reference_material)[1]
            reference_material_count = fromRoman(reference_material_roman)

        except Exception:
            print(f"{Fore.RED}{Style.BRIGHT}[Wrong format]{Style.RESET_ALL}")

        else:
            new_file_name = f'{year}-{month}-{date}-{lesson_name}-{reference_material_count}{file_extension}'
            new_file_name = new_file_name.replace('_', '-').lower()

            file.rename(directory / new_file_name)

            print(f"Renamed to {Fore.GREEN}{Style.BRIGHT}{new_file_name}{Style.RESET_ALL}")

def main(arguments: list[str]) -> None:
    parsed_namespace = define_and_read_args(arguments)
    directory = parsed_namespace.directory or '.'
    glob = parsed_namespace.glob or '*'
    files_to_rename = get_files_to_rename(glob, Path(directory))
    rename(files_to_rename, Path(directory))


if __name__ == '__main__':
    main(argv[1:])