import uuid
from datetime import datetime
from pypdf import PdfReader
from document_schema import Document, Elements, FileTypeEnum
from parsers.base import BaseParser

class FallBackParser(BaseParser):
    async def parse(self, file_path: str) -> Document:
        reader = PdfReader(file_path)
        elements = []

        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()

            if page_text and page_text.strip():
                elements.append(
                    Elements(
                        element_id= str(uuid.uuid4()),
                        element_type = "text",
                        content = page_text.strip(),
                        metadata = {
                            "page": page_num+1,
                            "parser_used": "pypdf_fallback"
                        }
                    )
                )
        return Document(
            document_id=str(uuid.uuid4()),
            filename=file_path,
            file_type=FileTypeEnum.PDF,
            created_at = datatime.now(),
            metadata={
                "total_pages": len(reader.pages),
                "extraction_quality": "low_res_text_only"
            },
            elements=elements
        )
