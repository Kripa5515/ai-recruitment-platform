import pytest
from app.core.file_validation import (
    FileValidationError,
    validate_resume_file,
)


def test_valid_pdf_file():
    content = b"%PDF-1.7 sample pdf content"
    result = validate_resume_file(
        filename="resume.pdf",
        content_type="application/pdf",
        file_content=content,
    )
    assert result == "pdf"


def test_valid_docx_file():
    content = b"PK\x03\x04sample docx content"

    result = validate_resume_file(
        filename="resume.docx",
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
        file_content=content,
    )
    assert result == "docx"


def test_reject_unsupported_extension():
    content = b"some file content"

    with pytest.raises(FileValidationError):
        validate_resume_file(
            filename="resume.exe",
            content_type="application/octet-stream",
            file_content=content,
        )


def test_reject_invalid_pdf_content():
    content = b"This is not a real PDF"

    with pytest.raises(FileValidationError):
        validate_resume_file(
            filename="resume.pdf",
            content_type="application/pdf",
            file_content=content,
        )


def test_reject_invalid_docx_content():
    content = b"This is not a real DOCX"

    with pytest.raises(FileValidationError):
        validate_resume_file(
            filename="resume.docx",
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            file_content=content,
        )


def test_reject_wrong_content_type():
    content = b"%PDF-1.7 sample pdf content"

    with pytest.raises(FileValidationError):
        validate_resume_file(
            filename="resume.pdf",
            content_type="text/plain",
            file_content=content,
        )


def test_reject_large_file():
    content = b"%PDF" + b"x" * (10 * 1024 * 1024)

    with pytest.raises(FileValidationError):
        validate_resume_file(
            filename="large_resume.pdf",
            content_type="application/pdf",
            file_content=content,
        )