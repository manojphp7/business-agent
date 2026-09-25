from pypdf import PdfReader
from backend.services.chunker import create_chunks

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def process_pdf(file_path: str):
    text = extract_text_from_pdf(file_path)

    chunks = create_chunks(text)

    return chunks