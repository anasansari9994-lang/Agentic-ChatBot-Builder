import uuid
from datetime import datetime
from unstructured.partition.pdf import partition_pdf
from document_schema import Document, Elements
from pathlib import Path
# from services.image_services import generate_description
from models.analysis_funciotn.image_analyser import describe_chart
from models.analysis_funciotn.table_analyser import generate_table_description
from core.logging import logger
from parsers.base import BaseParser

from io import StringIO
import pandas as pd

class PdfParser(BaseParser):
    async def parse(self, file_path:str) -> Document:
        logger.info("the PdfParser is runing----")
        document_id = str(uuid.uuid4())
        image_dir = Path("storage/images") / document_id
        image_dir.mkdir(parents=True, exist_ok=True)

        elements = partition_pdf(
            filename = file_path,
            strategy = "hi_res",
            infer_table_structure = True,
            extract_image_block_types=["Image", "Table"],
            extract_image_block_to_payload=False,
            extract_image_block_output_dir= str(image_dir)
        )

        unified_elements = []

        for el in elements:
            logger.info("text extraction running in pdf")
            el_type = "text"
            content = el.text

            if el.category == "Table":
                logger.info("table extraction running in pdf")
                el_type = "table"
                html = el.metadata.text_as_html
                if html:
                    dfs = pd.read_html(StringIO(html))
                    table_df = dfs[0]
                    content = table_df.to_markdown(index=False)
                    table_summary = generate_table_description(content)
                    content = table_summary
                    print(table_summary[:50])
                else:
                    content = el.text

            elif el.category == "Image":
                logger.info("image extraction running in pdf")
                el_type = "image"
                try:
                    image_path = Path(el.metadata.image_path)
                    description = describe_chart(str(image_path))
                    content = description
                    print(content[:50])
                except Exception as e:
                    logger.error("error in processing image")
                    content = ""

            unified_elements.append(
                Elements(
                    element_id = str(uuid.uuid4()),
                    element_type = el_type,
                    content = content,
                    metadata = {
                        "page" : el.metadata.page_number,
                        "coordinates" : getattr(el.metadata, "coordinates", None)
                    }
                )
            )
        return Document(
            document_id = document_id,
            filename = file_path,
            file_type = "pdf",
            created_at = datetime.now(),
            metadata = {"total_elements" : len(unified_elements)},
            elements = unified_elements
        )

