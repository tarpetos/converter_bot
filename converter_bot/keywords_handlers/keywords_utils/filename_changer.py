import os
from typing import Tuple


class RecursiveFilenameChanger:
    def __new__(cls, path: str) -> str:
        cls.__ADD_VAL: int = 0
        cls.__DIR_NAME: str = ""
        return cls.change(path)

    @classmethod
    def change(cls, path: str) -> str:
        cls.__DIR_NAME = os.path.dirname(path)
        if os.path.exists(path):
            file, ext = cls._get_file_params(path)
            new_filename = cls._get_unique_filename(os.path.basename(file))
            return cls.change(
                f"{os.path.join(cls.__DIR_NAME, new_filename)}{cls.__ADD_VAL if cls.__ADD_VAL else 1}{ext}"
            )
        return path

    @classmethod
    def _get_file_params(cls, path: str) -> Tuple[str, str]:
        has_ext_start: bool = "." in path
        file, ext = (path.split(".", maxsplit=1)) if has_ext_start else (path, "")
        ext = f".{ext}" if has_ext_start else ""
        return file, ext

    @classmethod
    def _get_unique_filename(cls, filename: str) -> str:
        if not filename:
            return filename

        for index, char in enumerate(filename):
            try:
                cls.__ADD_VAL = int(filename[index:]) + 1
                return filename[:index]
            except ValueError:
                if index == len(filename) - 1:
                    return filename
                continue
