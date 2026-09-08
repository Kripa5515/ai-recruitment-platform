from io import BytesIO

import fitz
from docx import Document

from app.services.exceptions import (
    DOCXExtractionError,
    PDFExtractionError,
)


def extract_pdf_text(file_content: bytes) -> str:
    """
    Extract text from a PDF file.

    Args:
        file_content: PDF file content as bytes.

    Returns:
        Extracted text as a string.

    Raises:
        PDFExtractionError:
            If the PDF cannot be opened or text extraction fails.
    """
    try:
        document = fitz.open(
            stream=file_content,
            filetype="pdf",
        )

        text_parts: list[str] = []

        for page in document:
            page_text = page.get_text()

            if page_text:
                text_parts.append(page_text)

        document.close()

        extracted_text = "\n".join(text_parts).strip()

        if not extracted_text:
            raise PDFExtractionError(
                "PDF does not contain extractable text."
            )

        return extracted_text

    except PDFExtractionError:
        raise

    except Exception as exc:
        raise PDFExtractionError(
            f"Failed to extract text from PDF: {exc}"
        ) from exc


def extract_docx_text(file_content: bytes) -> str:
    """
    Extract text from a DOCX file.

    Args:
        file_content: DOCX file content as bytes.

    Returns:
        Extracted text as a string.

    Raises:
        DOCXExtractionError:
            If the DOCX cannot be opened or text extraction fails.
    """
    try:
        document = Document(
            BytesIO(file_content)
        )

        text_parts: list[str] = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                text_parts.append(text)

        extracted_text = "\n".join(text_parts).strip()

        if not extracted_text:
            raise DOCXExtractionError(
                "DOCX does not contain extractable text."
            )

        return extracted_text

    except DOCXExtractionError:
        raise

    except Exception as exc:
        raise DOCXExtractionError(
            f"Failed to extract text from DOCX: {exc}"
        ) from exc