import json
import uuid
from pathlib import Path
from app.models.document import Document

EDUE_DATA_DIR = Path("data")
EDUE_DATA_DIR.mkdir(exist_ok=True)


def save_edue_document(document: Document) -> str:
    document_id = str(uuid.uuid4())
    file_path = EDUE_DATA_DIR / f"{document_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(document.model_dump(), f, indent=2)

    return document_id
