import uuid
from document_schema import Document, FileTypeEnum
from parsers.base import BaseParser

from parsers.pdf_parser import PdfParser
from parsers.fallback_pdf_parser import FallBackParser
from core.logging import logger

class PdfRoutingParser(BaseParser):
    def __init__(self):
        """
        The Connector Class.
        Instantiates both of your pre-written parsers as internal workers.
        """
        self.advanced_parser = PdfParser()
        self.fallback_parser = FallBackParser()

    async def parse(self, file_path: str) -> Document:
        logger.info(f"Routing PDF processing for file: {file_path}")
        document_id = str(uuid.uuid4())
        
        try:
            logger.info("Routing to Primary Engine: Advanced Unstructured...")
            parsed_doc = self.advanced_parser.parse(file_path)
            
            if parsed_doc.metadata.get("total_elements", 0) > 0:
                return parsed_doc
                
            logger.warning("Advanced engine returned 0 elements. Redirecting to fallback...")
            
        except Exception as error:
            logger.error(
                f"Advanced Engine failed or PDF is corrupted. Error: {str(error)}. "
                f"Connecting to PyPDF Fallback Safety Net..."
            )

        try:
            logger.info("Routing to Secondary Engine: PyPDF Fallback...")
            fallback_doc = self.fallback_parser.parse(file_path)
            
            fallback_doc.metadata["recovered_from_corruption_or_empty"] = True
            return fallback_doc
            
        except Exception as catastrophic_error:
            logger.critical(f"Catastrophic Ingestion Failure: File is completely unreadable. {str(catastrophic_error)}")
            return self._build_empty_document(document_id, file_path, FileTypeEnum.PDF)