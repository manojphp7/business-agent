from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector

from backend.database import Base


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(Vector(768), nullable=False)