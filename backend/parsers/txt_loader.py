import uuid
import os 
from datetime import datetime
from document_schema import Document, Elements, FileTypeEnum, ElementTypeEnum
from parsers.base import BaseParser
from core.logging import logger

class TextParser:
    def __init__(self, chunk_size: int = 10000, chunk_overlap: int = 1000):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    async def parse(self, file_path: str) -> Document:
        logger.inof("Text Parser is running")
        document_id = str(uuid.uuid4())
        unified_elements = []

        with open(file_path, "r", encoding='utf-8', errors="replace") as file:
            raw_text = file.read()
            if not raw_text.strip():
                logger.warning(f"Text file '{file_path}' is empty.")
                return self._build_empty_document(doc_id=document_id, path=file_path)

            chunks = self._chunk_text(text=raw_text, size=self.chunk_size, overlap=self.chunk_overlap)
            for idx,chunk_content in enumerate(chunks):
                unified_elements.append(
                    Elements(
                        element_id = str(uuid.uuid4()),
                        element_type = ElementTypeEnum.TEXT,
                        content = chunk_content,
                        metadata = {
                            "chunk_indez" : idx,
                            "total_chunks" : len(chunks),
                            "character_count" : len(chunk_content)
                        }
                    )
                )
        return Document(
            document_id = document_id,
            filename = os.path.basename(file_path),
            file_type = FileTypeEnum.TEXT,
            created_at = datetime.now(),
            metadata = {
                "file_size_bytes": os.path.getsize(file_path),
                "total_elements": len(unified_elements),
                "chunk_size_configured": self.chunk_size,
                "chunk_overlap_configured": self.chunk_overlap
            },
            elements = unified_elements
        )   


    def _chunk_text(self, text: str, size: int, overlap: int) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + size
            chunks.append(text[start:end])
            start += (size - overlap)
        return chunks

    def _build_empty_document(self, doc_id: str, path: str) -> Document:
        return Document(
            document_id=doc_id,
            filename=os.path.basename(path),
            file_type=FileTypeEnum.TEXT,
            created_at=datetime.now(),
            metadata={"total_elements": 0},
            elements=[]
        )