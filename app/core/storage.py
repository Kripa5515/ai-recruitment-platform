from pathlib import Path

from app.core.config import settings


def get_resume_storage_path() -> Path:
    storage_path = Path(settings.STORAGE_ROOT)
    storage_path.mkdir(parents=True, exist_ok=True)
    return storage_path


def save_resume_file(
    filename: str,
    file_content: bytes,
) -> Path:
    storage_path = get_resume_storage_path()

    file_path = storage_path / filename

    try:
        file_path.resolve().relative_to(storage_path.resolve())
    except ValueError:
        raise ValueError("Invalid filename: path traversal is not allowed.")

    file_path.write_bytes(file_content)

    return file_path