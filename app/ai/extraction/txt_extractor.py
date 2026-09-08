def extract_txt_text(file_content: bytes) -> str:
    """
    Extract text from a UTF-8 TXT byte stream.

    Args:
        file_content: TXT file content as bytes.

    Returns:
        Extracted text.

    Raises:
        ValueError: If the file cannot be decoded or is empty.
    """

    try:
        extracted_text = file_content.decode("utf-8").strip()

    except UnicodeDecodeError as exc:
        raise ValueError(
            "TXT file must be UTF-8 encoded."
        ) from exc

    if not extracted_text:
        raise ValueError(
            "TXT file does not contain any text."
        )

    return extracted_text