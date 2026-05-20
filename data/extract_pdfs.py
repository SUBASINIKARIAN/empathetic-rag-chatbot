"""
Extracts text from all PDFs in data/pdfs/ and writes data/knowledge_base.json.
Run: python data/extract_pdfs.py
Requires: pip install pymupdf
"""

import json
import os
import fitz  # PyMuPDF

PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
OUTPUT = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

CATEGORY_MAP = {
    "wellness": "mental_health",
    "burnout": "mental_health",
    "remote": "work_policy",
    "hr_leave": "benefits",
    "ai_tools": "ai_policy",
}


def infer_category(filename: str) -> str:
    name = filename.lower().replace(".pdf", "")
    for key, cat in CATEGORY_MAP.items():
        if key in name:
            return cat
    return "general"


def extract_pdfs(pdf_dir: str) -> list[dict]:
    documents = []
    pdf_files = sorted(f for f in os.listdir(pdf_dir) if f.endswith(".pdf"))

    for i, filename in enumerate(pdf_files, start=1):
        path = os.path.join(pdf_dir, filename)
        doc = fitz.open(path)

        pages_text = [page.get_text() for page in doc]
        full_text = "\n".join(pages_text).strip()

        title = filename.replace(".pdf", "").replace("_", " ").title()
        category = infer_category(filename)

        documents.append({
            "id": f"doc_{i:03d}",
            "title": title,
            "content": full_text,
            "category": category,
            "source": filename,
        })
        print(f"Extracted [{category}]: {filename} ({len(full_text)} chars)")

    return documents


if __name__ == "__main__":
    docs = extract_pdfs(PDF_DIR)
    with open(OUTPUT, "w") as f:
        json.dump(docs, f, indent=2)
    print(f"\nSaved {len(docs)} documents -> {OUTPUT}")
