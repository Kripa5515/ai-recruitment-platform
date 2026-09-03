import pymupdf
from app.services.exceptions import PDFExtractionError

def extract_pdf_text(file_content: bytes) -> str:
    """
    Extract text from a PDF byte stream.

    Args:
        file_content: PDF file content as bytes.

    Returns:
        Extracted text from all PDF pages.

    Raises:
        PDFExtractionError: If the PDF cannot be opened or processed.
    """

    try:
        document = pymupdf.open(
            stream=file_content,
            filetype="pdf",
        )

        try:
            pages_text = []

            for page in document:
                text = page.get_text()

                if text:
                    pages_text.append(text)

            return "\n".join(pages_text).strip()

        finally:
            document.close()

    except Exception as exc:
        raise PDFExtractionError(
            "Failed to extract text from PDF."
        ) from exc