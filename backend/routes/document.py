from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
from backend.services.document_processor import process_pdf
from backend.services.embedding import create_embedding
from backend.services.retrieval import search_similar_chunks
from backend.services.generation import generate_answer
from backend.models import DocumentEmbedding
from backend.database import SessionLocal
import shutil

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # PDF ko chunks mein convert karo
    chunks = process_pdf(str(file_path))

    # Database session
    db = SessionLocal()

    try:
        for index, chunk in enumerate(chunks):

            # Chunk ka vector banao
            embedding = create_embedding(chunk)

            # Database record banao
            document_embedding = DocumentEmbedding(
                filename=file.filename,
                chunk_index=index,
                chunk_text=chunk,
                embedding=embedding
            )

            # DB mein add karo
            db.add(document_embedding)

        # Saare records ek saath save
        db.commit()

    finally:
        db.close()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "total_chunks": len(chunks),
        "message": "Document embeddings saved successfully"
    }


@router.get("/")
async def get_documents():

    db = SessionLocal()

    try:
        documents = (
            db.query(DocumentEmbedding.filename)
            .distinct()
            .all()
        )

        return {
            "documents": [doc[0] for doc in documents]
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