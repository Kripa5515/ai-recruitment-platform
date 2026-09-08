def similarity_to_score(similarity: float) -> float:
    """
    Convert cosine similarity (-1 to 1)
    into a semantic score (0 to 100).
    """

    if not -1.0 <= similarity <= 1.0:
        raise ValueError(
            "Similarity must be between -1.0 and 1.0."
        )

    score = ((similarity + 1.0) / 2.0) * 100.0

    return round(score, 2)