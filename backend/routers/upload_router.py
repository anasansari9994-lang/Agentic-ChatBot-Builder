import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from document_schema import Document, FileTypeEnum
from core.logging import logger
from parsers_connection.connecter import ParserConnector
#router end poit
router = APIRouter(prefix="/ingestion", tags=["ingestion Engine"])
UPLOAD_TEMP_DIR = Path("storages/uploaded_files")
UPLOAD_TEMP_DIR.mkdir(parents=True, exist_ok=True)

@router.post(
    "/upload",
    response_model = Document,
    summary="Upload and extract text, tables, and images from any supported document format."
)
async def upload_and_parse(file: UploadFile = File(...)) -> Document:
    logger.info(f"Received upload request for file: {file.filename}")
    file_ext = os.path.splitext(file.filename)[1]
    if not file_ext:
        supported_format = ', '.join(f"{fr.value}" for fr in FileTypeEnum)
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"File must contain a valid extension format -> {supported_format}"
        )
    parser = ParserConnector.get_parser(file_ext)
    logger.info(f"the parser is selected for {file_ext}")
        
    local_file_path = UPLOAD_TEMP_DIR / file.filename

    try:
        with local_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Saved temp file to disk at: {local_file_path}. Commencing extraction...")

        parsed_document = await parser.parse(str(local_file_path))
        return parsed_document
    except Exception as e:
        logger.critical(f"Pipeline execution crash for {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failure: {str(e)}"
        )
    finally:
        if local_file_path.exists():
            os.remove(local_file_path)
            logger.info(f"Cleaned up raw temporary file from: {local_file_path}")