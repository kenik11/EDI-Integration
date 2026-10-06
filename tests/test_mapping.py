from pathlib import Path

from src.edi_intergration.parser.edi_parser import parse_edi
from src.edi_intergration.mapping.order_mapper import map_purchase_order


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FILE = PROJECT_ROOT / "data" / "inbound" / "order_1001.edi"


def load_sample_edi():
    return SAMPLE_FILE.read_text(encoding="utf-8")


def test_map_purchase_order_number():
    raw_edi = load_sample_edi()

    segments = parse_edi(raw_edi)
    order = map_purchase_order(segments)

    assert order["purchase_order"]["number"] == "PO10001"


def test_map_customer():
    raw_edi = load_sample_edi()

    segments = parse_edi(raw_edi)
    order = map_purchase_order(segments)

    assert order["customer"]["name"] == "ABC RETAIL"
    assert order["customer"]["id"] == "CUST001"


def test_map_supplier():
    raw_edi = load_sample_edi()

    segments = parse_edi(raw_edi)
    order = map_purchase_order(segments)

    assert order["supplier"]["name"] == "XYZ SUPPLIES"
    assert order["supplier"]["id"] == "SUP001"


def test_map_line_items():
    raw_edi = load_sample_edi()

    segments = parse_edi(raw_edi)
    order = map_purchase_order(segments)

    assert len(order["items"]) == 2

    assert order["items"][0]["sku"] == "ABC123"
    assert order["items"][0]["quantity"] == "10"

    assert order["items"][1]["sku"] == "XYZ456"
    assert order["items"][1]["quantity"] == "5"