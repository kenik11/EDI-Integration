def map_purchase_order(segments: list[list[str]]) -> dict:
    """
    Map parsed X12 EDI segments into a business-oriented
    purchase order structure.
    """

    purchase_order = {
        "purchase_order": {},
        "customer": {},
        "supplier": {},
        "items": []
    }

    for segment in segments:
        segment_id = segment[0]



      # Purchase order information
        if segment_id == "BEG":
            purchase_order["purchase_order"]["number"] = segment[3]
            purchase_order["purchase_order"]["date"] = segment[5]

        # Party information
        elif segment_id == "N1":
            entity_identifier = segment[1]
            name = segment[2]
            identification_code = segment[4]

            if entity_identifier == "BY":
                purchase_order["customer"]["name"] = name
                purchase_order["customer"]["id"] = identification_code

            elif entity_identifier == "ST":
                purchase_order["supplier"]["name"] = name
                purchase_order["supplier"]["id"] = identification_code

        # Line items
        elif segment_id == "PO1":
            item = {
                "line_number": segment[1],
                "quantity": segment[2],
                "unit": segment[3],
                "unit_price": segment[4],
                "product_qualifier": segment[6],
                "sku": segment[7]
            }

            purchase_order["items"].append(item)

    return purchase_order