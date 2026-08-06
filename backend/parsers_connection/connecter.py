from typing import Dict
from document_schema import Document, Elements, ElementTypeEnum, FileTypeEnum
from parsers.base import BaseParser
from parsers.xlsc_loader import ExcelParser
from parsers.PdfRoutingParser import PdfRoutingParser
from parsers.csv_loader import CsvParser
from parsers.markdown_loader import MarkdownParser
from parsers.docx_parser import DOCXParser

class ParserConnector:
    _parser: Dict[FileTypeEnum, BaseParser]={
        FileTypeEnum.PDF: PdfRoutingParser(),
        FileTypeEnum.DOCX: DOCXParser(),
        FileTypeEnum.XLSX: ExcelParser(),
        FileTypeEnum.CSV: CsvParser(),
        FileTypeEnum.MD: MarkdownParser()
    }
    @classmethod
    def get_parser(cls, file_extention: str) -> BaseParser:
        clean_text = file_extention.lower().lstrip('.')
        enum_type = FileTypeEnum(clean_text)
        return cls._parser[enum_type]