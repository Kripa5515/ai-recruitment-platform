import pytest
import pymupdf
from app.services.exceptions import PDFExtractionError
from app.ai.extraction.pdf_extractor import extract_pdf_text


def create_test_pdf() -> bytes:
    document = pymupdf.open()

    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Kripa Kumar\n"
        "Senior PHP Laravel Developer\n"
        "Python GenAI RAG Developer\n"
        "Skills: PHP, Laravel, Python, PostgreSQL",
    )

    pdf_bytes = document.tobytes()
    document.close()

    return pdf_bytes


def create_multi_page_pdf() -> bytes:
    document = pymupdf.open()

    page_1 = document.new_page()
    page_1.insert_text(
        (72, 72),
        "Page One - Professional Summary",
    )

    page_2 = document.new_page()
    page_2.insert_text(
        (72, 72),
        "Page Two - Work Experience",
    )

    page_3 = document.new_page()
    page_3.insert_text(
        (72, 72),
        "Page Three - Education",
    )

    pdf_bytes = document.tobytes()
    document.close()

    return pdf_bytes


def create_empty_pdf() -> bytes:
    document = pymupdf.open()

    document.new_page()

    pdf_bytes = document.tobytes()
    document.close()

    return pdf_bytes


def test_extract_pdf_text():
    pdf_bytes = create_test_pdf()

    extracted_text = extract_pdf_text(pdf_bytes)

    assert "Kripa Kumar" in extracted_text
    assert "Senior PHP Laravel Developer" in extracted_text
    assert "Python GenAI RAG Developer" in extracted_text
    assert "PostgreSQL" in extracted_text


def test_extract_pdf_text_from_multiple_pages():
    pdf_bytes = create_multi_page_pdf()

    extracted_text = extract_pdf_text(pdf_bytes)

    assert "Page One - Professional Summary" in extracted_text
    assert "Page Two - Work Experience" in extracted_text
    assert "Page Three - Education" in extracted_text


def test_extract_pdf_text_from_empty_pdf():
    pdf_bytes = create_empty_pdf()

    extracted_text = extract_pdf_text(pdf_bytes)

    assert extracted_text == ""


def test_extract_pdf_text_with_invalid_pdf():
    invalid_pdf = b"This is not a valid PDF file."

    with pytest.raises(PDFExtractionError):
        extract_pdf_text(invalid_pdf)

def test_extract_pdf_text_from_image_only_pdf():
    document = pymupdf.open()

    page = document.new_page()

    # Page intentionally contains no text layer.
    # This simulates an image-only/scanned PDF.
    pdf_bytes = document.tobytes()

    document.close()

    extracted_text = extract_pdf_text(pdf_bytes)

    assert extracted_text == ""