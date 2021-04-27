import pathlib
import sys
from typing import List, Set
from myapp.app import main


class File:
    str_match = 'this is a match\n'
    str_other = "this isn't a match\n"

    def __init__(
        self, path: pathlib.Path, matching_lines: List[int], max_lines: int, touch: bool
    ):
        """
        :param path: pathlib.Path to file
        :param matching_lines: number of lines that contain str_match
        :param max_lines: overall number of lines in file
        :param touch: if true, create file with given path
        """

        self.path = path
        self.matching_liens = matching_lines
        self.max_lines = max_lines

        if touch:
            self.touch(write=True)

    @staticmethod
    def write_to_file(
        file_path: pathlib.Path,
        str_match: str,
        str_other: str,
        matching_lines: List[int],
        max_lines: int,
    ):
        """
        :param file_path: pathlib.Path to file
        :param str_match: string that should match the given regex
        :param str_other: string that should not math the given regex
        :param matching_lines: number of lines that contain str_match
        :param max_lines: overall number of lines in file
        """
        with file_path.open('a', encoding='utf-8') as file:
            for cur_line in range(1, max_lines + 1):
                if cur_line in matching_lines:
                    file.write(str_match)
                else:
                    file.write(str_other)

    @staticmethod
    def create_files(
        path: pathlib.Path,
        filenames: List[str],
        matching_lines: List[List[int]],
        max_lines: List[int],
        touch: bool,
    ):
        """
        methods for creating several files in the given path

        filenames: list of filenames
        matching_lines: list of matching lines for each file
        max_lines: list of max lines for each file
        touch: bool
        """
        files = []
        for index, file in enumerate(filenames):
            new_file = File(
                path=path / file,
                matching_lines=matching_lines[index],
                max_lines=max_lines[index],
                touch=touch,
            )
            files.append(new_file)

        return files

    def touch(self, write: bool):
        self.path.touch()
        if write:
            File.write_to_file(
                file_path=self.path,
                str_match=File.str_match,
                str_other=File.str_other,
                matching_lines=self.matching_liens,
                max_lines=self.max_lines,
            )


def check_output(files: List[File], output: Set[str], tmp_path: pathlib.Path):
    """
    function for testing if the output to console is correct
    """
    for file in files:
        path = file.path.relative_to(tmp_path.absolute())
        for match in file.matching_liens:
            result = f'{path} line={match}: {File.str_match[:-1]}'
            output.discard(result)
    return len(output) == 0


def run_main(path, regex) -> None:
    """
    function for running main with corresponding sys.args
    """
    # saving old values of sys.argv
    before = sys.argv.copy()
    sys.argv = ['mygrep', path, regex]
    main()
    # reverting changes
    sys.argv = before
