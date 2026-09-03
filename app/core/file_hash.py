import hashlib

def calculate_sha256(file_content: bytes) -> str:
    """
    Calculate SHA-256 hash of file content.
    """
    return hashlib.sha256(file_content).hexdigest()