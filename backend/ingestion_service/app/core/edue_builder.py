import re
import pdfplumber
from app.models.document import Document, Section, ContentLine

COURSE_CODE_PATTERN = re.compile(r"\b[A-Z]{2}\s?[A-Z]{1,2}\d{3}\b")


def build_edue_document(pdf_path: str) -> Document:
    sections = []
    current_section = None
    document_title = None

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages, start=1):
            lines = page.extract_text().splitlines() if page.extract_text() else []

            for line in lines:
                text = line.strip()
                if not text:
                    continue

                # 🔹 Detect course code like AE ZG631
                if COURSE_CODE_PATTERN.search(text):
                    if current_section:
                        current_section.end_page = page_index
                        sections.append(current_section)

                    current_section = Section(
                        title=text,
                        start_page=page_index,
                        end_page=page_index,
                        content=[]
                    )

                    if not document_title:
                        document_title = text

                else:
                    if current_section:
                        current_section.content.append(
                            ContentLine(
                                text=text,
                                page_number=page_index
                            )
                        )

        if current_section:
            current_section.end_page = page_index
            sections.append(current_section)

    return Document(
        title=document_title,
        sections=sections
    )
