import os
import shutil
from typing import Final, List

import pytest
from _pytest.fixtures import FixtureRequest, FixtureFunction

from converter_bot.keywords_handlers.keywords_utils.filename_changer import RecursiveFilenameChanger

CURRENT_DIR: Final[str] = os.path.dirname(__file__)


@pytest.fixture(scope="function")
def prep_dir() -> str:
    test_dir_path: str = os.path.join(CURRENT_DIR, "test_data")
    if not os.path.exists(test_dir_path) and not os.path.isdir(test_dir_path):
        os.mkdir(test_dir_path)

    yield test_dir_path

    shutil.rmtree(test_dir_path, ignore_errors=True)


@pytest.fixture(scope="function")
def prep_file(prep_dir: FixtureFunction, request: FixtureRequest) -> str:
    test_dir_path = prep_dir
    filename = getattr(request, "param", "test.txt")
    test_file: str = os.path.join(test_dir_path, filename)

    with open(test_file, "w"):
        ...

    return RecursiveFilenameChanger(test_file)


@pytest.fixture(scope="function")
def prep_files(prep_dir: FixtureFunction, request: FixtureRequest) -> List[str]:
    filename = getattr(request, "param", "test.txt")
    test_file = os.path.join(prep_dir, filename)

    files = []
    for i in range(10):
        with open((actual_path := RecursiveFilenameChanger(test_file)), "w"):
            ...
        files.append(os.path.basename(actual_path))

    return files
