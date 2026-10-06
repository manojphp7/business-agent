from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
from backend.services.document_processor import process_pdf
from backend.services.embedding import create_embedding
from backend.services.retrieval import search_similar_chunks
from backend.services.generation import generate_answer
from backend.models import DocumentEmbedding, Company
from backend.database import SessionLocal
import shutil
import os
from fastapi.responses import FileResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    agent_key: str = Form("")
):

    if not agent_key:
        raise HTTPException(
            status_code=400,
            detail="Agent key is required"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    db = SessionLocal()

    try:
        # Find company
        company = db.query(Company).filter(
            Company.agent_key == agent_key
        ).first()

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Invalid agent key"
            )

        # --------------------------------
        # Company-specific folder
        # --------------------------------

        upload_dir = Path(
            f"data/uploads/company_{company.id}"
        )

        upload_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = upload_dir / file.filename

        # --------------------------------
        # Remove old embeddings
        # for this company + file
        # --------------------------------

        db.query(DocumentEmbedding).filter(
            DocumentEmbedding.company_id == company.id,
            DocumentEmbedding.filename == file.filename
        ).delete(
            synchronize_session=False
        )

        # --------------------------------
        # Save / overwrite PDF
        # --------------------------------

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # --------------------------------
        # Process PDF
        # --------------------------------

        chunks = process_pdf(
            str(file_path)
        )

        # --------------------------------
        # Create embeddings
        # --------------------------------

        for index, chunk in enumerate(chunks):

            embedding = create_embedding(chunk)

            document_embedding = DocumentEmbedding(
                filename=file.filename,
                chunk_index=index,
                chunk_text=chunk,
                embedding=embedding,
                company_id=company.id
            )

            db.add(document_embedding)

        db.commit()

        return {
            "filename": file.filename,
            "company_id": company.id,
            "company_name": company.name,
            "total_chunks": len(chunks),
            "message": "Document uploaded successfully"
        }

    finally:
        db.close()



@router.get("/search")
async def search_documents(query: str):

    results = search_similar_chunks(query)

    return {
    "query": query,
    "results": [
        {
            "filename": result.filename,
            "chunk_index": result.chunk_index,
            "chunk_text": result.chunk_text,
            "distance": distance
        }
        for result, distance in results
    ]
}


@router.get("/ask")
async def ask_question(query: str):

    results = search_similar_chunks(query)

    context = "\n\n".join(
        result.chunk_text
        for result, distance in results
    )

    answer = generate_answer(query, context)

    return {
        "query": query,
        "answer": answer,
        "sources": [
            {
                "filename": result.filename,
                "chunk_index": result.chunk_index,
                "distance": distance
            }
            for result, distance in results
        ]
    }

@router.get("/")
async def get_documents(agent_key: str):

    db = SessionLocal()

    try:
        company = db.query(Company).filter(
            Company.agent_key == agent_key
        ).first()

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Invalid agent key"
            )

        upload_dir = Path(
            f"data/uploads/company_{company.id}"
        )

        if not upload_dir.exists():
            return {
                "documents": []
            }

        documents = []

        for file_path in upload_dir.iterdir():

            if file_path.is_file():

                documents.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified_at": file_path.stat().st_mtime
                })

        return {
            "company_id": company.id,
            "company_name": company.name,
            "documents": documents
        }

    finally:
        db.close()

@router.get("/download/{filename:path}")
async def download_document(
    filename: str,
    agent_key: str
):
    db = SessionLocal()

    try:
        company = db.query(Company).filter(
            Company.agent_key == agent_key
        ).first()

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Invalid agent key"
            )

        upload_dir = Path(
            f"data/uploads/company_{company.id}"
        )

        file_path = upload_dir / filename

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return FileResponse(
            path=file_path,
            filename=file_path.name,
            media_type="application/pdf"
        )

    finally:
        db.close()

@router.delete("/{filename:path}")
async def delete_document(
    filename: str,
    agent_key: str
):
    db = SessionLocal()

    try:
        company = db.query(Company).filter(
            Company.agent_key == agent_key
        ).first()

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Invalid agent key"
            )

        upload_dir = Path(
            f"data/uploads/company_{company.id}"
        )

        file_path = upload_dir / filename

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        # Delete embeddings/chunks
        db.query(DocumentEmbedding).filter(
            DocumentEmbedding.company_id == company.id,
            DocumentEmbedding.filename == filename
        ).delete(
            synchronize_session=False
        )

        # Delete physical PDF
        file_path.unlink()

        db.commit()

        return {
            "filename": filename,
            "message": "Document deleted successfully"
        }

    finally:
        db.close()