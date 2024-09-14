import os


class RecursiveFilenameChanger:
    __ADD_VAL: int = 0
    __DIR_NAME: str = ""

    def __new__(cls, path: str) -> str:
        return cls.change(path)

    @classmethod
    def change(cls, path: str) -> str:
        cls.__DIR_NAME = os.path.dirname(path)
        if os.path.exists(path):
            file, ext = os.path.splitext(path)
            new_filename = cls._get_unique_filename(os.path.basename(file))
            return cls.change(
                f"{os.path.join(cls.__DIR_NAME, new_filename)}{cls.__ADD_VAL if cls.__ADD_VAL else 1}{ext}"
            )
        return path

    @classmethod
    def _get_unique_filename(cls, filename: str) -> str:
        for index, char in enumerate(filename):
            try:
                cls.__ADD_VAL = int(filename[index:]) + 1
                return filename[:index]
            except ValueError:
                if index == len(filename) - 1:
                    return filename
                continue
