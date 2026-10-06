from backend.database import SessionLocal
from backend.models import DocumentEmbedding
from backend.services.embedding import create_embedding


def search_similar_chunks(
    query: str,
    company_id: int = None,
    limit: int = 5,
    max_distance: float = 0.60
):
    query_embedding = create_embedding(query)

    db = SessionLocal()

    try:
        query_obj = db.query(
            DocumentEmbedding,
            DocumentEmbedding.embedding.cosine_distance(
                query_embedding
            ).label("distance")
        )

        # Company ID diya hai to sirf us company ke documents search karo
        if company_id is not None:
            query_obj = query_obj.filter(
                DocumentEmbedding.company_id == company_id
            )

        results = (
            query_obj
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