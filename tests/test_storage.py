from pathlib import Path
from app.core.storage import (
    get_resume_storage_path,
    save_resume_file,
)
import pytest

def test_resume_storage_path_exists():
    storage_path = get_resume_storage_path()

    assert isinstance(storage_path, Path)
    assert storage_path.exists()
    assert storage_path.is_dir()

def test_save_resume_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    file_content = b"sample resume content"
    filename = "test_resume.pdf"

    saved_path = save_resume_file(
        filename=filename,
        file_content=file_content,
    )

    assert saved_path.exists()
    assert saved_path.is_file()
    assert saved_path.read_bytes() == file_content


def test_save_resume_file_creates_storage_directory(tmp_path, monkeypatch):
    storage_path = tmp_path / "resumes"

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(storage_path),
    )

    assert not storage_path.exists()

    saved_path = save_resume_file(
        filename="resume.pdf",
        file_content=b"resume data",
    )

    assert storage_path.exists()
    assert saved_path.exists()


def test_save_resume_file_returns_path(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    saved_path = save_resume_file(
        filename="candidate.pdf",
        file_content=b"candidate resume",
    )

    assert isinstance(saved_path, Path)
    assert saved_path.name == "candidate.pdf"

def test_save_resume_file_rejects_path_traversal(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    with pytest.raises(ValueError):
        save_resume_file(
            filename="../../secret.txt",
            file_content=b"malicious content",
        )