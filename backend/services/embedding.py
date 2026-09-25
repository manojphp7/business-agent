import ollama


def create_embedding(chunk: str):
    result = ollama.embed(
        model="nomic-embed-text",
        input=chunk
    )

    return result["embeddings"][0]