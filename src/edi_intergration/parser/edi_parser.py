def parse_edi(raw_edi: str) -> list[list[str]]:
    """
    Parse a basic X12 EDI document.

    Assumptions:
    - "~" is the segment terminator
    - "*" is the element separator

    Returns:
        A list of EDI segments, where each segment is
        represented as a list of elements.
    """

    # Split the document into individual segments
    segments = raw_edi.strip().split("~")

    parsed_segments = []

    for segment in segments:
        segment = segment.strip()

        # Ignore empty segments
        if not segment:
            continue

        # Split each segment into elements
        elements = segment.split("*")

        parsed_segments.append(elements)

    return parsed_segments