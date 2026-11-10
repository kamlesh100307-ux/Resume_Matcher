from io import BytesIO
from pathlib import Path
import fitz
from docx import Document

def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    extension = Path(filename).suffix.lower()
    if extension == ".pdf":
        with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
            text = "\n".join(page.get_text() for page in pdf)
    elif extension == ".docx":
        document = Document(BytesIO(file_bytes))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    else:
        raise ValueError("Unsupported file type. Upload PDF or DOCX.")
    if not text.strip():
        raise ValueError("No readable text found. Scanned PDFs need OCR, not included here.")
    return text
