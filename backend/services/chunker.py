def create_chunks(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        # Agar poora text khatam ho gaya
        if end >= len(text):
            chunks.append(text[start:].strip())
            break

        # Chunk ko newline ya sentence ke end par todne ki koshish
        split_position = text.rfind("\n", start, end)

        if split_position <= start:
            split_position = text.rfind(". ", start, end)

        if split_position <= start:
            split_position = end

        chunk = text[start:split_position].strip()

        if chunk:
            chunks.append(chunk)

        start = split_position - overlap

    return chunks