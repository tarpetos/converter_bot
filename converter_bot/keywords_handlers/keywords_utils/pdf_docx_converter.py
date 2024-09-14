import os
from typing import List, Tuple, Optional, Union

import pypandoc
from pdf2docx import Converter

from .constants import DOCUMENT_FILE_PREFIX, PDF, DEFAULT_RESULT_FILE_NAME, DOCX
from .filer_loader import FileLoader
from .image_to_file_converter import FileConverter


class DocumentLoader(FileLoader):
    async def save_files(self, file_ids: List[str], **kwargs) -> List[str]:
        file_extension = kwargs["file_extension"]
        document_list = await self._documents_processing(file_ids, file_extension=file_extension)
        return document_list

    async def _documents_processing(self, file_ids: List[str], file_extension: Optional[str] = None) -> List[str]:
        return await self._process_files(file_ids, DOCUMENT_FILE_PREFIX, file_extension)


class DocxToPdf(FileConverter):
    def convert(self, conversion_file_path: str, paths: List[str], **kwargs) -> None:
        pdf_file = os.path.join(paths[0], f"{DEFAULT_RESULT_FILE_NAME}.{PDF}")
        pypandoc.convert_file(conversion_file_path, PDF, outputfile=pdf_file)


class PdfToDocx(FileConverter):
    def convert(
        self,
        conversion_file_path: str,
        paths: List[str],
        password: Optional[str] = None,
        **kwargs,
    ) -> None:
        docx_file = os.path.join(paths[0], f"{DEFAULT_RESULT_FILE_NAME}.{DOCX}")
        conversion_file = Converter(conversion_file_path, password=password)
        conversion_file.convert(docx_file)
        conversion_file.close()
