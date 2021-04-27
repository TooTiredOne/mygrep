import re
import sys
from pathlib import Path


def filter_lines(file_path: Path, regex: str):
    """
    generator for returning lines of files matching regex

    :param file_path: pathlib.Path
    :param regex: str

    returns number of the line matching the regex, and the line itself
    """

    try:
        with file_path.open() as file:
            # reading line by line
            pattern = re.compile(regex)
            for index, line in enumerate(file, start=1):
                if pattern.search(line):
                    yield index, line.rstrip()
    # for ignoring binary files
    except UnicodeDecodeError:
        return


class UserException(Exception):
    pass


def parse_args(args):
    """
    function for reading arguments
    """

    if len(args) != 3:
        raise UserException(
            "Incorrect arguments\nPlease, run 'myapp [path] [substring]'"
        )

    path = Path(args[1])
    regex = args[2]

    if not path.exists():
        raise UserException(f"path {path} doesn't exists")

    return path, regex


def main():
    try:
        init_path, substr = parse_args(sys.argv)
    except UserException as e:
        print(e)
        return

    # if path to file
    if init_path.is_file():
        for line_numb, line_text in filter_lines(init_path, substr):
            print(f'{init_path} line={line_numb}: {line_text}')

        return

    # if path to dir
    for cur_path in init_path.glob('**/*'):
        if cur_path.is_file():
            for line_numb, line_text in filter_lines(cur_path, substr):
                print(
                    f'{cur_path.relative_to(init_path)} line={line_numb}: {line_text}'
                )
