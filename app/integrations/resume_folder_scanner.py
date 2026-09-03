from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
}

def scan_resume_folder(
    folder_path: str | Path,
) -> list[Path]:
    """
    Scan a folder and return supported resume files.

    Supported formats:
    - PDF
    - DOCX

    Only files directly inside the given folder are scanned.
    Subdirectories are ignored.
    """
    folder = Path(folder_path)
    if not folder.exists():
        raise ValueError(
            f"Resume folder does not exist: {folder}"
        )
    if not folder.is_dir():
        raise ValueError(
            f"Resume path is not a directory: {folder}"
        )
    resume_files = [
        path
        for path in folder.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(resume_files)