import os
from typing import Union, Optional, Tuple, Dict, Any

from aiogram import types
from aiogram.types import ContentType, PhotoSize, Document

from .constants import (
    MAIN_TEMP_DATA_FOLDER,
    USER_FOLDER_NAME_PREFIX,
    DOCX,
    DOC,
    PDF,
    JPEG,
    JPG,
    PNG,
)
from .pdf_docx_converter import DocxToPdf, PdfToDocx


def get_conversion_path_name(
    dir_type: str,
    user_id: int,
    file_ext: Optional[str] = None,
    filename: Optional[str] = None,
) -> str:
    path = os.path.join(
        MAIN_TEMP_DATA_FOLDER,
        f"{USER_FOLDER_NAME_PREFIX}_{dir_type}_{user_id}",
        f"{filename}.{file_ext}" if file_ext and filename else "",
    )
    return os.path.abspath(path)


def is_file_ext_allowed(message: types.Message, allowed_extensions: Tuple[str, str, str]) -> bool:
    document_extension = message.document.file_name.split(".")[-1]
    return document_extension in allowed_extensions


def get_opposite_ext_params(ext: str) -> Dict[str, Union[str, Any]]:
    params = (PDF, DocxToPdf) if ext in (DOC, DOCX) else (DOCX, PdfToDocx)
    return {
        "opposite_ext": params[0],
        "converter_cls": params[1],
    }


def is_document(message: types.Message) -> bool:
    return message.content_type == ContentType.DOCUMENT


def is_photo(message: types.Message) -> bool:
    return message.content_type == ContentType.PHOTO


def file_option_selector(
    message: types.Message,
) -> Union[PhotoSize, Optional[Document]]:
    if is_photo(message):
        return message.photo[-1]

    if is_file_ext_allowed(message, allowed_extensions=(JPEG, JPG, PNG)):
        return message.document


def parse_args(message: types.Message) -> Optional[int]:
    arg_list = message.text.strip().split(PDF)
    try:
        compression_level = int(arg_list[1])
    except ValueError:
        return None
    return compression_level


def change_filename(message: types.Message, conversion_extension: str) -> str:
    real_file_name = message.reply_to_message.document.file_name
    return f"{real_file_name.split('.')[0]}.{conversion_extension}"
