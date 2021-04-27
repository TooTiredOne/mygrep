import pytest
from myapp.app import UserException, filter_lines, parse_args
from .conftest import File, check_output, run_main


# test for filter_lines()
@pytest.mark.parametrize(
    ('matching_lines', 'max_lines'),
    [
        ([1, 2, 5], 5),  # several matches including first and last lines of the file
        ([4], 10),  # a single match somewhere in the middle of the file
        ([1, 2, 3, 6], 20),  # several matches
        ([], 4),  # no matches
    ],
)
def test_filter_match(tmp_path, matching_lines, max_lines):
    """
    test when path points to file and there are some/no matches

    tmp_path: pytest fixture
    matching_lines: list of lines containing matches
    max_lines: int, overall number of lines in the file
    """

    # make testing file
    file_path = tmp_path / 'test_file.txt'
    file_path.touch()

    # preparing the testing file
    str_match = 'this will match\n'
    str_other = 'no match here\n'

    File.write_to_file(
        file_path=file_path,
        str_match=str_match,
        str_other=str_other,
        matching_lines=matching_lines,
        max_lines=max_lines,
    )

    # obtaining numbers of lines with matches
    found_matches = [
        line_numb for line_numb, _ in filter_lines(file_path=file_path, regex=str_match)
    ]

    assert found_matches == matching_lines


# test for parse_args()
@pytest.mark.parametrize(
    'args',
    [
        ['mygrep'],  # no args
        ['mygrep', 'too few args'],  # too low number of args
        ['mygrep', 'too', 'many', 'args'],  # too big number of args
    ],
)
def test_parse_args_wrong_numb(args):
    """
    test when wrong amount of arguments is passed

    :param args: arguments to be passed in sys.argv
    :return:
    """

    with pytest.raises(UserException):
        parse_args(args)


# test for parse_args()
def test_parse_args_non_exist_path():
    """
    test when path argument points to non-existing file/dir

    :return:
    """
    # appending args containing path to non existing file/dir
    str_path = 'non/existing/path'
    str_regex = 'some regex'

    with pytest.raises(UserException):
        parse_args(['mygrep', str_path, str_regex])


# test for parse_args()
def test_parse_args_ok_path(tmp_path):
    """
    test when everything is ok with args

    :param tmp_path: pytest fixture
    :return:
    """
    # make testing file
    file_path = tmp_path / 'test_file.txt'
    file_path.touch()
    str_regex = 'some regex'
    path, regex = parse_args(['mygrep', file_path, str_regex])
    # checking out the output
    assert path == file_path and regex == str_regex


# test for main()
def test_main_path_to_file(tmp_path, capsys):
    """
    test when path points to a file

    :param tmp_path: pytest fixture
    :param capsys: pytest fixture
    """
    file_path = tmp_path / 'file'
    file_path.touch()
    str_regex = 'match\n'
    str_other = 'other\n'
    File.write_to_file(
        file_path=file_path,
        str_match=str_regex,
        str_other=str_other,
        matching_lines=[4],
        max_lines=10,
    )

    run_main(path=file_path, regex=str_regex)
    out, _ = capsys.readouterr()

    assert out.rstrip() == f'{file_path} line=4: match'


# test for main()
def test_main_binary(tmp_path, capsys):
    """
    test when path points to a binary file

    :param tmp_path: pytest fixture
    :param capsys: pytest fixture
    """
    file_path = tmp_path / 'file'
    file_path.touch()
    str_regex = 'char'
    file_path.write_bytes(b'evil \xe9 char')

    run_main(path=file_path, regex=str_regex)

    # checking the output
    out, _ = capsys.readouterr()

    assert out.rstrip() == ''


def test_main_ok_root_dir(tmp_path, capsys):
    """
    test 1st lvl of depth when everything is ok with args

    :param tmp_path: pytest fixture
    :param capsys: pytest fixture
    :return:
    """

    # creating files in root dir
    files = File.create_files(
        path=tmp_path,
        filenames=['f1', 'f2'],
        matching_lines=[[2, 5], []],
        max_lines=[10, 10],
        touch=True,
    )

    run_main(path=tmp_path.absolute(), regex=File.str_match)

    # checking the output
    out, _ = capsys.readouterr()
    # acquiring output lines
    out = set(out.split('\n')[:-1])

    assert check_output(files=files, output=out, tmp_path=tmp_path)


def test_main_ok_sub_dirs(tmp_path, capsys):
    """
    test 2nd lvl of depth when everything is ok with args

    :param tmp_path: pytest fixture
    :param capsys: pytest fixture
    :return:
    """

    files = []

    # creating /subdir1
    subdir1 = tmp_path / 'subdir1'
    subdir1.mkdir()
    # creating files in /subdir1
    files.extend(
        File.create_files(
            path=subdir1,
            filenames=['f1', 'f2', 'f3'],
            matching_lines=[[5], [8, 19, 20], []],
            max_lines=[14, 20, 20],
            touch=True,
        )
    )

    # creating /subdir2
    subdir2 = tmp_path / 'subdir2'
    subdir2.mkdir()
    # creating files in /subdir2
    files.extend(
        File.create_files(
            path=subdir2,
            filenames=['f1'],
            matching_lines=[[]],
            max_lines=[50],
            touch=True,
        )
    )

    run_main(path=tmp_path.absolute(), regex=File.str_match)

    # checking the output
    out, _ = capsys.readouterr()
    out = set(out.split('\n')[:-1])

    assert check_output(files=files, output=out, tmp_path=tmp_path)


# test for main()
def test_main_args_sub_sub_dirs(tmp_path, capsys):
    """
    test 3rd lvl of depth when everything is ok with args

    :param tmp_path: pytest fixture
    :param capsys: pytest fixture
    :return:
    """

    files = []

    # creating /subdir1/subdir2
    subdir1 = tmp_path / 'subdir1'
    subdir1.mkdir()
    subdir2 = subdir1 / 'subdir2'
    subdir2.mkdir()
    # creating files in /subdir2/subdir3
    files.extend(
        File.create_files(
            path=subdir2,
            filenames=['f1', 'f2'],
            matching_lines=[[], [5, 59, 70]],
            max_lines=[1000, 100],
            touch=True,
        )
    )

    run_main(path=tmp_path.absolute(), regex=File.str_match)

    # checking the output
    out, _ = capsys.readouterr()
    out = set(out.split('\n')[:-1])

    assert check_output(files=files, output=out, tmp_path=tmp_path)
