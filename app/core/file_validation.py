from pathlib import Path

ALLOWED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "docx",
}

ALLOWED_CONTENT_TYPES = {
    "pdf": {
        "application/pdf",
    },
    "docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/zip",
    },
}

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

class FileValidationError(ValueError):
    """Raised when an uploaded file fails validation."""

def validate_resume_file(
    filename: str,
    content_type: str | None,
    file_content: bytes,
) -> str:
    """
    Validate a resume file and return its normalized file type.

    Supported formats:
    - PDF
    - DOCX
    """

    extension = Path(filename).suffix.lower()

    # 1. Extension validation
    if extension not in ALLOWED_EXTENSIONS:
        raise FileValidationError(
            "Unsupported file type. Only PDF and DOCX files are allowed."
        )

    file_type = ALLOWED_EXTENSIONS[extension]

    # 2. File size validation
    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise FileValidationError(
            f"File size exceeds the maximum allowed limit of "
            f"{MAX_FILE_SIZE_MB} MB."
        )

    # 3. MIME type validation
    allowed_content_types = ALLOWED_CONTENT_TYPES[file_type]

    if content_type not in allowed_content_types:
        raise FileValidationError(
            f"Invalid content type for {file_type.upper()} file."
        )

    # 4. File signature/content validation
    if file_type == "pdf":
        if not file_content.startswith(b"%PDF"):
            raise FileValidationError(
                "Invalid PDF file content."
            )

    elif file_type == "docx":
        if not file_content.startswith(b"PK"):
            raise FileValidationError(
                "Invalid DOCX file content."
            )

    return file_type