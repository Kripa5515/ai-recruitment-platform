from pathlib import Path
from zipfile import BadZipFile, ZipFile

from app.ai.extraction.docx_extractor import extract_docx_text
from app.ai.extraction.job_extractor import JobExtractor
from app.ai.extraction.pdf_extractor import extract_pdf_text
from app.ai.extraction.txt_extractor import extract_txt_text
from app.api.schemas.job_requirements import JobRequirements
from app.services.exceptions import (
    DOCXExtractionError,
    PDFExtractionError,
)


class JobDocumentService:
    """
    Handles JD document validation, text extraction,
    and structured JD analysis.
    """

    ALLOWED_EXTENSIONS = {
        ".txt",
        ".pdf",
        ".docx",
    }

    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

    def __init__(self):
        self.extractor = JobExtractor()

    # =====================================================
    # File Validation
    # =====================================================

    def validate_file(
        self,
        filename: str,
        file_content: bytes,
    ) -> str:
        """
        Validate filename, extension, and file size.

        Returns:
            Normalized file extension without the dot.

        Raises:
            ValueError: If validation fails.
        """

        if not filename or not filename.strip():
            raise ValueError(
                "Filename is required."
            )

        extension = Path(filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                "Unsupported file type. "
                "Only TXT, PDF and DOCX files are allowed."
            )

        if not file_content:
            raise ValueError(
                "Uploaded file is empty."
            )

        if len(file_content) > self.MAX_FILE_SIZE_BYTES:
            raise ValueError(
                "File size exceeds the maximum allowed size of 10 MB."
            )

        return extension[1:]

    # =====================================================
    # File Signature Validation
    # =====================================================

    @staticmethod
    def validate_file_signature(
        file_type: str,
        file_content: bytes,
    ) -> None:
        """
        Validate the actual file signature.

        File extensions and MIME types can be spoofed,
        so we also inspect the file bytes.
        """

        if file_type == "pdf":
            if not file_content.startswith(b"%PDF-"):
                raise ValueError(
                    "Invalid PDF file."
                )

        elif file_type == "docx":
            if not file_content.startswith(b"PK"):
                raise ValueError(
                    "Invalid DOCX file."
                )

            try:
                with ZipFile(
                    __import__("io").BytesIO(file_content)
                ) as archive:

                    required_files = {
                        "[Content_Types].xml",
                        "word/document.xml",
                    }

                    archive_files = set(
                        archive.namelist()
                    )

                    missing_files = (
                        required_files - archive_files
                    )

                    if missing_files:
                        raise ValueError(
                            "Invalid DOCX file structure."
                        )

            except BadZipFile as exc:
                raise ValueError(
                    "Invalid DOCX file."
                ) from exc

    # =====================================================
    # Text Extraction
    # =====================================================

    def extract_text(
        self,
        file_type: str,
        file_content: bytes,
    ) -> str:
        """
        Extract plain text from TXT, PDF or DOCX.
        """

        try:
            if file_type == "txt":
                return extract_txt_text(
                    file_content
                )

            if file_type == "pdf":
                return extract_pdf_text(
                    file_content
                )

            if file_type == "docx":
                return extract_docx_text(
                    file_content
                )

            raise ValueError(
                f"Unsupported file type: {file_type}"
            )

        except PDFExtractionError:
            raise

        except DOCXExtractionError:
            raise

    # =====================================================
    # Analyze Uploaded JD
    # =====================================================

    def analyze_file(
    self,
    filename: str,
    file_content: bytes,
    ) -> JobRequirements:

        file_type = self.validate_file(
            filename,
            file_content,
        )

        self.validate_file_signature(
            file_type,
            file_content,
        )

        extracted_text = self.extract_text(
            file_type,
            file_content,
        )

        requirements = self.extractor.extract(
            extracted_text
        )

        requirements.extracted_text = extracted_text

        return requirements