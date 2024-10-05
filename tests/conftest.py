import os
import shutil
from typing import Final

import pytest

from converter_bot.keywords_handlers.keywords_utils.filename_changer import RecursiveFilenameChanger

CURRENT_DIR: Final[str] = os.path.dirname(__file__)


@pytest.fixture(scope="session")
def prep_dir() -> str:
    test_dir_path: str = os.path.join(CURRENT_DIR, "test_data")
    if not os.path.exists(test_dir_path) and not os.path.isdir(test_dir_path):
        os.mkdir(test_dir_path)

    yield test_dir_path

    shutil.rmtree(test_dir_path, ignore_errors=True)


@pytest.fixture(scope="function")
def prep_file(prep_dir, request) -> str:
    test_dir_path = prep_dir
    filename = getattr(request, "param", "test.txt")
    test_file: str = os.path.join(test_dir_path, filename)

    with open(test_file, "w"): ...

    return RecursiveFilenameChanger(test_file)
