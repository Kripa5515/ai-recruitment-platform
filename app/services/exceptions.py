class DuplicateResumeError(ValueError):
    """Raised when a resume with the same file hash already exists."""

class PDFExtractionError(ValueError):
    """Raised when PDF text extraction fails."""

class DOCXExtractionError(ValueError):
    """Raised when DOCX text extraction fails."""