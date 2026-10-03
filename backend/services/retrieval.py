from backend.database import SessionLocal
from backend.models import DocumentEmbedding
from backend.services.embedding import create_embedding


def search_similar_chunks(
    query: str,
    limit: int = 2,
    max_distance: float = 0.60
):
    query_embedding = create_embedding(query)

    db = SessionLocal()

    try:
        results = (
            db.query(
                DocumentEmbedding,
                DocumentEmbedding.embedding.cosine_distance(
                    query_embedding
                ).label("distance")
            )
            .filter(
                DocumentEmbedding.embedding.cosine_distance(
                    query_embedding
                ) <= max_distance
            )
            .order_by(
                DocumentEmbedding.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
            .all()
        )

        return results

    finally:
        db.close()