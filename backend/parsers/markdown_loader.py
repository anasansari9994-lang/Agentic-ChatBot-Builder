import asyncio
import os
import uuid
from datetime import datetime

from core.logging import logger
from document_schema import Document, Elements, FileTypeEnum
from parsers.base import BaseParser


class MarkdownParser(BaseParser):

    async def parse(self, file_path: str) -> Document:
        logger.info(f"Parsing Markdown file: {file_path}")

        document_id = str(uuid.uuid4())

        try:
            text = await asyncio.to_thread(self._read_markdown_file, file_path)

            element = Elements(
                element_id=str(uuid.uuid4()),
                element_type="text",
                content=text,
                metadata={}
            )

            return Document(
                document_id=document_id,
                filename=os.path.basename(file_path),
                file_type=FileTypeEnum.MD,      # or FileTypeEnum.MARKDOWN
                created_at=datetime.now(),
                metadata={
                    "file_size_bytes": os.path.getsize(file_path),
                    "total_elements": 1,
                    "is_empty": len(text.strip()) == 0
                },
                elements=[element]
            )

        except Exception as e:
            logger.exception(f"Failed to parse Markdown file: {e}")

            return self._build_empty_document(
                document_id=document_id,
                file_path=file_path,
                file_type=FileTypeEnum.MD  
            )

    @staticmethod
    def _read_markdown_file(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()