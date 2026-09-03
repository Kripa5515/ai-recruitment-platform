from pathlib import Path
import pytest
from app.integrations.resume_folder_scanner import scan_resume_folder

def test_scan_resume_folder_returns_pdf_and_docx(tmp_path: Path):
    pdf_file = tmp_path / "kripa.pdf"
    docx_file = tmp_path / "john.docx"
    txt_file = tmp_path / "notes.txt"

    pdf_file.write_bytes(b"fake pdf")
    docx_file.write_bytes(b"fake docx")
    txt_file.write_text("ignore me")

    result = scan_resume_folder(tmp_path)
    assert result == sorted(
        [
            pdf_file,
            docx_file,
        ]
    )

def test_scan_resume_folder_is_case_insensitive(tmp_path: Path):
    pdf_file = tmp_path / "resume.PDF"
    docx_file = tmp_path / "resume.DOCX"
    pdf_file.write_bytes(b"fake pdf")
    docx_file.write_bytes(b"fake docx")
    result = scan_resume_folder(tmp_path)
    assert result == sorted(
        [
            pdf_file,
            docx_file,
        ]
    )

def test_scan_resume_folder_ignores_subdirectories(
    tmp_path: Path,
):
    pdf_file = tmp_path / "resume.pdf"
    pdf_file.write_bytes(b"fake pdf")
    subdirectory = tmp_path / "old_resumes"
    subdirectory.mkdir()
    nested_pdf = subdirectory / "old.pdf"
    nested_pdf.write_bytes(b"fake pdf")
    result = scan_resume_folder(tmp_path)
    assert result == [pdf_file]


def test_scan_resume_folder_returns_empty_list_for_empty_folder(
    tmp_path: Path,
):
    result = scan_resume_folder(tmp_path)
    assert result == []


def test_scan_resume_folder_raises_for_missing_folder(
    tmp_path: Path,
):
    missing_folder = tmp_path / "does_not_exist"
    with pytest.raises(ValueError, match="does not exist"):
        scan_resume_folder(missing_folder)

def test_scan_resume_folder_raises_for_file_path(
    tmp_path: Path,
):
    file_path = tmp_path / "resume.pdf"
    file_path.write_bytes(b"fake pdf")
    with pytest.raises(ValueError, match="not a directory"):
        scan_resume_folder(file_path)