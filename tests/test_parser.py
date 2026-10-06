from pathlib import Path

from src.edi_intergration.parser.edi_parser import parse_edi


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Sample EDI file
SAMPLE_FILE = PROJECT_ROOT / "data" / "inbound" / "order_1001.edi"


def load_sample_edi():
    """Read the sample EDI document."""
    return SAMPLE_FILE.read_text(encoding="utf-8")


def test_parser_reads_edi_segments():
    """Verify that EDI segments are correctly identified."""

    raw_edi = load_sample_edi()

    segments = parse_edi(raw_edi)

    assert segments[0][0] == "ISA"
    assert segments[1][0] == "GS"
    assert segments[2][0] == "ST"


def test_parser_identifies_850_transaction():
    """Verify that the document is an EDI 850 transaction."""

    raw_edi = load_sample_edi()

    segments = parse_edi(raw_edi)

    transaction = segments[2]

    assert transaction[0] == "ST"
    assert transaction[1] == "850"
    assert transaction[2] == "0001"


def test_parser_reads_purchase_order():
    """Verify that the purchase order number and date are parsed."""

    raw_edi = load_sample_edi()

    segments = parse_edi(raw_edi)

    beg_segment = next(
        segment for segment in segments
        if segment[0] == "BEG"
    )

    assert beg_segment[3] == "PO10001"
    assert beg_segment[5] == "20261002"


def test_parser_reads_line_items():
    """Verify that both PO1 line items are parsed."""

    raw_edi = load_sample_edi()

    segments = parse_edi(raw_edi)

    po1_segments = [
        segment for segment in segments
        if segment[0] == "PO1"
    ]

    assert len(po1_segments) == 2

    # First item
    assert po1_segments[0][1] == "1"
    assert po1_segments[0][2] == "10"
    assert po1_segments[0][7] == "ABC123"

    # Second item
    assert po1_segments[1][1] == "2"
    assert po1_segments[1][2] == "5"
    assert po1_segments[1][7] == "XYZ456"