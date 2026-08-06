from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class FileTypeEnum(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    CSV = "csv"
    XLSX = "xlsx"
    TXT = "txt"
    MD = "md"

class ElementTypeEnum(str, Enum):
    TEXT = "text"
    TABLE = "table"
    IMAGE = "image"
    CHART = "chart"

class Elements(BaseModel):
    element_id: str = Field(..., description="Unique UUID string identifying this block")
    element_type: ElementTypeEnum = Field(..., description="The type classification of the content (must be: text, table, image, or chart)")
    content: str = Field(..., description="The raw string value extracted")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    class Config:
        from_attributes = True
    
class Document(BaseModel):
    document_id: str = Field(..., description="Unique UUID string identifying this file")
    filename: str = Field(..., description="The file extension category (must be: pdf, docx, csv, or xlsx)")
    file_type: FileTypeEnum
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    elements: List[Elements] = Field(default=[])
    class Config:
        from_attributes = True