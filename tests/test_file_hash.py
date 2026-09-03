from app.core.file_hash import calculate_sha256

def test_sha256_returns_expected_hash():
    content = b"hello world"
    result = calculate_sha256(content)
    assert result == (
        "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee"
        "9088f7ace2efcde9"
    )


def test_same_content_produces_same_hash():
    content = b"same resume content"
    hash_1 = calculate_sha256(content)
    hash_2 = calculate_sha256(content)
    assert hash_1 == hash_2


def test_different_content_produces_different_hash():
    hash_1 = calculate_sha256(b"resume version 1")
    hash_2 = calculate_sha256(b"resume version 2")
    assert hash_1 != hash_2


def test_sha256_length():
    result = calculate_sha256(b"test")
    assert len(result) == 64