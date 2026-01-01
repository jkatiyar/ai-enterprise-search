from typing import List
from dataclasses import dataclass


# --------------------------------------------------
# Line-level granularity (atomic evidence unit)
# --------------------------------------------------

@dataclass
class Line:
    text: str
    page_number: int


# --------------------------------------------------
# Section-level structure (course / chapter / heading)
# --------------------------------------------------

@dataclass
class Section:
    title: str
    content: List[Line]


# --------------------------------------------------
# Document root (EDUE + RAG source of truth)
# --------------------------------------------------

@dataclass
class Document:
    document_id: str
    filename: str
    sections: List[Section]
