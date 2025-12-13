from utils.file_utils import save_temp_file
from utils.pdf_parser import extract_text_from_pdf
from utils.text_chunker import chunk_text
from utils.db_utils import insert_document_metadata

async def process_file(file):
    file_path = save_temp_file(file)

    extracted_text = ""
    chunks = []

    if file.filename.lower().endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
        chunks = chunk_text(extracted_text)

    # Save metadata to DB
    insert_document_metadata(
        filename=file.filename,
        file_path=file_path,
        text_length=len(extracted_text),
        num_chunks=len(chunks),
    )

    return {
        "filename": file.filename,
        "saved_as": file_path,
        "text_length": len(extracted_text),
        "num_chunks": len(chunks),
        "message": "File uploaded, processed, and metadata stored successfully",
    }
