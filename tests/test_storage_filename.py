from app.core.storage_filename import generate_storage_filename

def test_generate_pdf_filename():
    file_hash = "a" * 64
    filename = generate_storage_filename(
        file_type="pdf",
        file_hash=file_hash,
    )
    assert filename == f"{file_hash}.pdf"


def test_generate_docx_filename():
    file_hash = "b" * 64
    filename = generate_storage_filename(
        file_type="docx",
        file_hash=file_hash,
    )
    assert filename == f"{file_hash}.docx"


def test_same_hash_generates_same_filename():
    file_hash = "c" * 64
    filename_1 = generate_storage_filename(
        file_type="pdf",
        file_hash=file_hash,
    )
    filename_2 = generate_storage_filename(
        file_type="pdf",
        file_hash=file_hash,
    )
    assert filename_1 == filename_2

def test_different_hash_generates_different_filename():
    filename_1 = generate_storage_filename(
        file_type="pdf",
        file_hash="d" * 64,
    )

    filename_2 = generate_storage_filename(
        file_type="pdf",
        file_hash="e" * 64,
    )

    assert filename_1 != filename_2