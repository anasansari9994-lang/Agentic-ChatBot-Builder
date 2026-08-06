import uuid
import os
from datetime import datetime
from io import StringIO
import pandas as pd

from document_schema import Elements, ElementTypeEnum, Document, FileTypeEnum
from parsers.base import BaseParser
from core.logging import logger

class ExcelParser(BaseParser):
    async def parse(self, file_path:str) -> Document:
        logger.info(f"The ExcelParser is executing for file: {file_path}")
        document_id = str(uuid.uuid4())
        unified_elements = []
        excel_file = pd.ExcelFile(file_path)
        for sheet_n in excel_file.sheet_names:
            logger.info((f"Processing sheet: {sheet_name}"))
            df = pd.read_excel(excel_file, sheet_name=sheet_n, dtype=str)
            if df.empty:
                logger.warning("sheet is empty")
                continue
            df = df.drop_duplicates()
            df = df.dropna(how="all").loc[:, ~df.columns.str.startswith('Unnamed:')]
            json_content = df.to_json(orient="records")

            sheet_metadat = {
                sheet_name: sheet_n,
                total_rows: len(df),
                total_columns: len(df.columns),
                columns: list(df.columns),
                missing_value_sum: df.isna().sum().to_dict()
            }

            unified_elements.append(
                Elements(
                    element_id = str(uuid.uuid4()),
                    element_type = ElementTypeEnum.TABLE,
                    content = json_content,
                    metadata=sheet_metadat
                )
            )

        return Document(
            document_id = document_id,
            filename = os.path.basename(file_path),
            file_type = FileTypeEnum.XLSX,
            created_at = datetime.now(),
            metadata={
                "total_sheets" : len(excel_file.sheet_names),
                "total_elements" : len(unified_elements)
            },
            elements = unified_elements
        )