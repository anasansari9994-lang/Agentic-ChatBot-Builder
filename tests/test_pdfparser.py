import pytest
from llama_index.core import Document
from tests.dataset import SAMPLE_PDF
from backend.parsers.pdf_parser import PdfParser

def test_pdf_parser():
    assert SAMPLE_PDF.exists(), f"Mock PDF not found at {SAMPLE_PDF}"
    document = PdfParser(str(SAMPLE_PDF))
    assert isinstance(document, list)
    assert len(document) > 0

    first_doc = document[0]
    assert isinstance(first_doc, document)

    assert len(first_doc.text) > 10 