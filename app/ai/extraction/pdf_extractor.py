import fitz

from app.services.exceptions import PDFExtractionError


def extract_pdf_text(file_content: bytes) -> str:
    """
    Extract text from a PDF byte stream.

    Args:
        file_content: PDF file content as bytes.

    Returns:
        Extracted text from all PDF pages.

    Raises:
        PDFExtractionError: If the PDF cannot be opened,
        processed, or contains no extractable text.
    """

    try:
        document = fitz.open(
            stream=file_content,
            filetype="pdf",
        )

        try:
            text_parts = []

            for page in document:
                text = page.get_text().strip()

                if text:
                    text_parts.append(text)

            extracted_text = "\n".join(text_parts).strip()

        finally:
            document.close()

        if not extracted_text:
            raise PDFExtractionError(
                "PDF does not contain extractable text."
            )

        return extracted_text

    except PDFExtractionError:
        raise

    except Exception as exc:
        raise PDFExtractionError(
            "Failed to extract text from PDF."
        ) from exc