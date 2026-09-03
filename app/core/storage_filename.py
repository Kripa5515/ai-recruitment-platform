from uuid import uuid4

def generate_storage_filename(
    file_type: str,
    file_hash: str,
) -> str:
    return f"{file_hash}.{file_type}"