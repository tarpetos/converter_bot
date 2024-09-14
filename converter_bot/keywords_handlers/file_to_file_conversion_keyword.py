import os
import re
from typing import Dict, Union

from aiogram import F, types

from .keywords_utils.constants import (
    DOCUMENTS_FOLDER,
    DOCX,
    DOC,
    PDF,
    DEFAULT_RESULT_FILE_NAME,
)
from .keywords_utils.document_checks import (
    is_document,
    is_file_ext_allowed,
    get_conversion_path_name,
    change_filename,
    get_opposite_ext_params,
)
from .keywords_utils.file_size_controller import is_document_sent
from .keywords_utils.pdf_docx_converter import DocumentLoader
from ..config import dp


@dp.message(
    F.reply_to_message
    & F.text.regexp(
        re.compile(
            r"^convert$|^конвертуй$",
            re.IGNORECASE,
        ),
    )
)
async def keyword_img_to_file_handler(message: types.Message) -> None:
    replied_message = message.reply_to_message
    if is_document(replied_message):
        await process_img_to_file_keyword(message, replied_message)


async def process_img_to_file_keyword(message: types.Message, replied_message: types.Message) -> None:
    document_server_id = replied_message.document.file_id
    file_ext = replied_message.document.file_name.split(".")[-1]

    if not is_file_ext_allowed(replied_message, allowed_extensions=(DOCX, DOC, PDF)):
        return

    file_loader = DocumentLoader(message, DOCUMENTS_FOLDER)
    document_path_list = await file_loader.save_files([document_server_id], file_extension=file_ext)
    document_absolute_path = os.path.abspath(document_path_list[0])
    user_id = message.from_user.id
    folder_path = get_conversion_path_name(DOCUMENTS_FOLDER, user_id)

    bot_reply_data = await send_file(message, file_ext, document_absolute_path, folder_path, user_id)
    bot_message = bot_reply_data["message"]
    is_sent = bot_reply_data["is_sent"]

    await bot_message.edit_text(
        "Conversion failed with error!"
        if is_sent == -1
        else (
            "Conversion was successfully ended!" if is_sent else
            "Conversion failed because converted file is larger than 50MB!"
        )
    )

    file_loader.remove_temp_dir()


async def send_file(
    message: types.Message,
    current_ext: str,
    document_absolute_path: str,
    folder_path: str,
    user_id: int,
) -> Dict[str, Union[types.Message, bool]]:
    target_params = get_opposite_ext_params(current_ext)
    target_ext, converter_cls = target_params["opposite_ext"], target_params["converter_cls"]

    bot_message = await message.reply(f"{current_ext.upper()} to {target_ext.upper()} conversion started...")
    file_to_file = converter_cls()
    status = file_to_file.convert(document_absolute_path, [folder_path])
    if status == -1:
        return {
            "message": bot_message,
            "is_sent": status,
        }
    file_to_send = get_conversion_path_name(DOCUMENTS_FOLDER, user_id, target_ext, filename=DEFAULT_RESULT_FILE_NAME)

    new_filename = change_filename(message, target_ext)
    is_sent = await is_document_sent(message, file_to_send, new_filename)

    return {
        "message": bot_message,
        "is_sent": is_sent,
    }
