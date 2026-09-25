from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from backend.services.document_processor import process_pdf
import shutil

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = process_pdf(str(file_path))

    return {
        "filename": file.filename,
    "content_type": file.content_type,
    "chunks": chunks,
    "total_chunks": len(chunks)
    }