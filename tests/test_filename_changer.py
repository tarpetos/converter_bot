import os

import pytest


@pytest.mark.parametrize(
    "prep_file, expected_filename",
    [
        ("test.txt", "test1.txt"),
        ("test", "test1"),
        ("test.", "test1."),
        ("test.tar.gz", "test1.tar.gz"),
        ("test.docx.pdf.exe", "test1.docx.pdf.exe"),
        ("test0.txt", "test1.txt"),
        ("test0", "test1"),
        ("test0.", "test1."),
        ("test0.tar.gz", "test1.tar.gz"),
        ("test0.docx.pdf.exe", "test1.docx.pdf.exe"),
        ("test1.txt", "test2.txt"),
        ("test1", "test2"),
        ("test1.", "test2."),
        ("test1.tar.gz", "test2.tar.gz"),
        ("test1.docx.pdf.exe", "test2.docx.pdf.exe"),
        ("test2.txt", "test3.txt"),
        ("test2", "test3"),
        ("test2.", "test3."),
        ("test2.tar.gz", "test3.tar.gz"),
        ("test2.docx.pdf.exe", "test3.docx.pdf.exe"),
        ("test10.txt", "test11.txt"),
        ("test10", "test11"),
        ("test10.", "test11."),
        ("test10.tar.gz", "test11.tar.gz"),
        ("test10.docx.pdf.exe", "test11.docx.pdf.exe"),
        (".txt", "1.txt"),
        (".tar.gz", "1.tar.gz"),
        (".docx.pdf.exe", "1.docx.pdf.exe"),
    ],
    indirect=["prep_file"],
)
def test_filename_changer(prep_file, expected_filename):
    path = prep_file
    assert (
        actual_filename := os.path.basename(path)
    ) == expected_filename, f"Expected filename must be `{expected_filename}`, got `{actual_filename}` instead!"


def test_filename_changer_many(prep_files):
    actual_names = prep_files
    expected_names = [f"test{i if i != 0 else ""}.txt" for i in range(10)]
    assert (
        actual_names == expected_names
    ), f"Expected list of filenames must be `{expected_names}`, got `{actual_names}` instead!"


@pytest.mark.parametrize(
    "prep_file, expected_filename",
    [
        (".", IsADirectoryError),
        ("", IsADirectoryError),
    ],
    indirect=["prep_file"],
)
@pytest.mark.xfail(raises=IsADirectoryError)
def test_invalid_filename(prep_file, expected_filename): ...
