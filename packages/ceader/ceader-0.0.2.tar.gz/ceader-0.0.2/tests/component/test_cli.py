# fmt: off
import sys
import tempfile
from pathlib import Path

import pytest

from ceader.__main__ import run_cli
from ceader.domain.knowledge.extensions_to_language import \
    EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING
from ceader.domain.utils import get_file_lines
from tests import TEST_HEADER_PATH


# fmt: on
def test_cli_add_header() -> None:

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
        assert (len(get_file_lines(Path(file_1.name)))) == 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "add_header",
            "--files-dir",
            str(tmpdirname),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions-list",
            ".py",
            "--debug",
        ]
        run_cli()
        assert (len(get_file_lines(Path(file_1.name)))) > 0
        file_1.close()


def test_cli_add_and_remove_header() -> None:

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
        assert (len(get_file_lines(Path(file_1.name)))) == 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "add_header",
            "--files-dir",
            str(tmpdirname),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions-list",
            ".py",
            "--debug",
        ]
        run_cli()
        assert (len(get_file_lines(Path(file_1.name)))) > 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "remove_header",
            "--files-dir",
            str(tmpdirname),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions-list",
            ".py",
            "--debug",
        ]
        run_cli()
        assert (len(get_file_lines(Path(file_1.name)))) == 0
        file_1.close()


def test_cli_not_dir() -> None:
    with pytest.raises(ValueError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_1 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)

            assert (len(get_file_lines(Path(file_1.name)))) == 0
            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "add_header",
                "--files-dir",
                str(TEST_HEADER_PATH.resolve()),
                "--header-path",
                str(TEST_HEADER_PATH.resolve()),
                "--extensions-list",
                ".py",
                "--debug",
            ]
            run_cli()


def test_cli_not_file() -> None:
    with pytest.raises(ValueError):
        with tempfile.TemporaryDirectory() as tmpdirname:

            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "add_header",
                "--files-dir",
                str(tmpdirname),
                "--header-path",
                str(tmpdirname),
                "--extensions-list",
                ".py",
                "--debug",
            ]
            run_cli()


def test_cli_add_and_remove_header_all_ext() -> None:
    for ext in EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING.keys():
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_1 = tempfile.NamedTemporaryFile(suffix=ext, dir=tmpdirname)
            assert (len(get_file_lines(Path(file_1.name)))) == 0

            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "add_header",
                "--files-dir",
                str(tmpdirname),
                "--header-path",
                str(TEST_HEADER_PATH.resolve()),
                "--extensions-list",
                f"{ext}",
                "--debug",
            ]
            run_cli()
            assert (len(get_file_lines(Path(file_1.name)))) > 0

            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "remove_header",
                "--files-dir",
                str(tmpdirname),
                "--header-path",
                str(TEST_HEADER_PATH.resolve()),
                "--extensions-list",
                f"{ext}",
                "--debug",
            ]
            run_cli()
            assert (len(get_file_lines(Path(file_1.name)))) == 0
            file_1.close()


# def test_cli_get_print_python() -> None:

#     with tempfile.TemporaryDirectory() as tmpdirname:
#         file = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
#         file.write(b"print('Hello world!')")
#         file.flush()
#         file.seek(0)
#         assert(len(get_file_lines(Path(file.name)))) == 1


#         sys.argv = [
#             "--foo", # to make sure that test works. We ignore first argv using MakeFile
#             "--mode",
#             "add_header",
#             "--files-dir",
#              str(tmpdirname),
#             "--header-path",
#             str(TEST_HEADER_PATH.resolve()),
# 		    "--extensions-list",
#             ".py",
# 		    "--debug"
#         ]
#         run_cli()

#         for line in get_file_lines(Path(file.name)):
#             print(line.replace("\n",""))

#         print()
#         #assert(len(get_file_lines(Path(file.name)))) == 0
#         result = StringIO(initial_value=(str(os.system(f'python {Path(file.name)}'))))
#         print(result.getvalue(),"HA")
#         assert False

# python -m pytest tests/component/test_cli.py
