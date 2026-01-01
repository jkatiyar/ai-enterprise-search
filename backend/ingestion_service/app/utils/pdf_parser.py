import pdfplumber
import re
from typing import List, Dict


# ============================================================
# COURSE-SPECIFIC LOGIC (unchanged, preserved)
# ============================================================

COURSE_HEADER_PATTERN = re.compile(
    r"(AE\*?\s*ZG\d{3})\s+(.+?)\s+(\d)$"
)


def normalize_course_code(text: str) -> str:
    text = text.upper().replace("*", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_courses_from_pdf(file_path: str) -> List[Dict]:
    """
    Layout-aware course extractor.
    Returns structured course entities with page numbers.
    """

    courses = []

    with pdfplumber.open(file_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(use_text_flow=True)

            if not words:
                continue

            page_width = page.width
            mid_x = page_width / 2

            left_col = [w for w in words if w["x0"] < mid_x]
            right_col = [w for w in words if w["x0"] >= mid_x]
            columns = [c for c in (left_col, right_col) if c]

            page_lines = []

            for col in columns:
                col.sort(key=lambda w: (w["top"], w["x0"]))
                line, last_top = "", None

                for w in col:
                    if last_top is None or abs(w["top"] - last_top) < 5:
                        line += " " + w["text"]
                    else:
                        page_lines.append(line.strip())
                        line = w["text"]
                    last_top = w["top"]

                if line.strip():
                    page_lines.append(line.strip())

            current_course = None

            for line in page_lines:
                match = COURSE_HEADER_PATTERN.match(line)
                if match:
                    if current_course:
                        courses.append(current_course)

                    code_raw, title, credits = match.groups()
                    current_course = {
                        "course_code": normalize_course_code(code_raw),
                        "title": title.strip(),
                        "credits": int(credits),
                        "description": "",
                        "page": page_idx,
                    }
                elif current_course:
                    current_course["description"] += " " + line

            if current_course:
                courses.append(current_course)

    return courses


# ============================================================
# GENERIC DOCUMENT PARSER (NEW)
# ============================================================

GENERIC_HEADER_PATTERN = re.compile(
    r"^[A-Z][A-Za-z0-9\s\-:,]{3,}$"
)


def extract_structured_sections_from_pdf(file_path: str) -> List[Dict]:
    """
    Generic header + paragraph extractor.
    Works for books, research papers, specs, manuals.
    """

    sections: List[Dict] = []
    current_section = None

    with pdfplumber.open(file_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            lines = [l.strip() for l in text.split("\n") if l.strip()]

            for line in lines:
                # Heuristic: header lines
                is_header = (
                    len(line) < 120
                    and GENERIC_HEADER_PATTERN.match(line)
                    and line.isupper()
                )

                if is_header:
                    if current_section:
                        sections.append(current_section)

                    current_section = {
                        "title": line,
                        "paragraphs": [],
                        "pages": [page_idx],
                    }
                else:
                    if not current_section:
                        current_section = {
                            "title": "Introduction",
                            "paragraphs": [],
                            "pages": [page_idx],
                        }

                    current_section["paragraphs"].append(line)
                    if page_idx not in current_section["pages"]:
                        current_section["pages"].append(page_idx)

        if current_section:
            sections.append(current_section)

    return sections


# ============================================================
# AUTO-DETECTOR (used by ingest_service)
# ============================================================

def auto_extract_pdf(file_path: str) -> Dict:
    """
    Automatically chooses the best extraction strategy.
    """

    courses = extract_courses_from_pdf(file_path)

    if courses:
        return {
            "type": "course_catalog",
            "sections": [
                {
                    "title": f"{c['course_code']} {c['title']}",
                    "paragraphs": [c["description"]],
                    "pages": [c["page"]],
                }
                for c in courses
            ],
        }

    # Fallback to generic parsing
    sections = extract_structured_sections_from_pdf(file_path)
    return {
        "type": "generic_document",
        "sections": sections,
    }
