import uuid
from typing import Dict, List

from app.utils.file_utils import save_temp_file
from app.utils.pdf_parser import extract_structured_sections_from_pdf
from app.utils.db_utils import insert_document_metadata


# -------------------------------------------------------------------
# In-memory EDUE document store (can be DB later)
# -------------------------------------------------------------------

EDUE_DOCUMENT_STORE: Dict[str, Dict] = {}


# -------------------------------------------------------------------
# Ingestion entrypoint
# -------------------------------------------------------------------

def process_file(file):
    """
    Generic PDF ingestion for EDUE.

    - Supports ANY PDF (courses, books, research papers)
    - Builds semantic sections (header + paragraphs)
    """

    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported")

    file_path = save_temp_file(file)
    document_id = str(uuid.uuid4())

    # ---------------------------------------------------------------
    # Extract GENERIC semantic structure (not courses!)
    # ---------------------------------------------------------------

    sections = extract_structured_sections_from_pdf(file_path)

    if not sections:
        raise ValueError("No readable content found in PDF")

    # ---------------------------------------------------------------
    # Persist in EDUE store
    # ---------------------------------------------------------------

    EDUE_DOCUMENT_STORE[document_id] = {
        "document_id": document_id,
        "filename": file.filename,
        "sections": sections,   # 🔑 KEY CHANGE
    }

    # ---------------------------------------------------------------
    # Metadata for DB / observability
    # ---------------------------------------------------------------

    total_text_len = sum(
        len(p)
        for sec in sections
        for p in sec.get("paragraphs", [])
    )

    insert_document_metadata(
        filename=file.filename,
        file_path=file_path,
        text_length=total_text_len,
        num_chunks=len(sections),
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "saved_as": file_path,
        "sections_extracted": len(sections),
        "message": "File uploaded, processed, and EDUE document created successfully",
    }


# -------------------------------------------------------------------
# Document fetch
# -------------------------------------------------------------------

def get_document_by_id(document_id: str):
    return EDUE_DOCUMENT_STORE.get(document_id)
