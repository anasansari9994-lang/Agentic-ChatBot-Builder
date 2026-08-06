from abc import ABC, abstractmethod
from datetime import datetime
import os

from document_schema import Document, FileTypeEnum


class BaseParser(ABC):

    @abstractmethod
    def parse(self, file_path: str) -> Document:
        pass

    def _build_empty_document(
        self,
        document_id: str,
        file_path: str,
        file_type: FileTypeEnum,
    ) -> Document:

        return Document(
            document_id=document_id,
            filename=os.path.basename(file_path),
            file_type=file_type,
            created_at=datetime.now(),
            metadata={
                "file_size_bytes": os.path.getsize(file_path),
                "total_elements": 0,
                "is_empty": True,
            },
            elements=[],
        )