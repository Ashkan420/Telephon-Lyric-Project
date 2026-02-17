def split_text_by_line_breaks(text: str, limit: int = 3425):
    """
    Splits `text` into chunks of max `limit` characters.
    Splits ONLY at the nearest line break before the limit.
    """
    text = text.strip()
    chunks = []

    while text:
        if len(text) <= limit:
            chunks.append(text)
            break

        # Find the last line break within the limit
        cut = text.rfind("\n\n", 0, limit)
        if cut == -1:
            # No line break found before limit, force split at limit
            cut = limit

        chunk = text[:cut].rstrip()
        chunks.append(chunk)
        text = text[cut:].lstrip("\n")  # remove leading newlines from next chunk

    return chunks
