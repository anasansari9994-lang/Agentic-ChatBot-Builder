import uuid
import os
from datetime import datetime

import pandas as pd

from document_schema import (
    Document,
    Elements,
    FileTypeEnum,
    ElementTypeEnum,
)
from parsers.base import BaseParser
from core.logging import logger


class CsvParser(BaseParser):

    async def parse(self, file_path: str) -> Document:
        logger.info(f"CsvParser is executing for file: {file_path}")

        document_id = str(uuid.uuid4())
        unified_elements = []

        try:
        
            df = pd.read_csv(file_path, dtype=str)

            df = df.dropna(how="all")

            df = df.loc[:, ~df.columns.str.startswith("Unnamed:")]

            if df.empty:
                logger.warning(f"CSV file '{file_path}' is empty.")

                return self._build_empty_document(
                    document_id=document_id,
                    file_path=file_path,
                    file_type=FileTypeEnum.CSV
                )

            json_content = df.to_json(
                orient="records",
                force_ascii=False
            )

            unified_elements.append(
                Elements(
                    element_id=str(uuid.uuid4()),
                    element_type=ElementTypeEnum.TABLE,
                    content=json_content,
                    metadata={
                        "total_rows": len(df),
                        "total_columns": len(df.columns),
                        "columns": list(df.columns),
                        "character_count": len(json_content)
                    }
                )
            )

        except Exception:
            logger.exception(f"Critical error parsing CSV file: {file_path}")
            raise

        return Document(
            document_id=document_id,
            filename=os.path.basename(file_path),
            file_type=FileTypeEnum.CSV,
            created_at=datetime.now(),
            metadata={
                "file_size_bytes": os.path.getsize(file_path),
                "total_elements": len(unified_elements)
            },
            elements=unified_elements
        )