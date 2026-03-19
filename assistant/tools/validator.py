REQUIRED_FIELDS = [
    "contract_value",
    "responsible",
    "category_description",
    "account_description",
    "suppliers",
    "supplier_name",
    "description_supplier",
    "owner_gt",
    "termination",
    "valid_from",
    "valid_to",
    "ongoing",
]


def validate_contract_fields(fields: dict) -> dict:
    """Checks which required contract fields are missing or empty.

    Args:
        fields: A dict of field names to extracted values.

    Returns:
        A dict with 'missing' (list of empty/absent fields),
        'populated' (list of fields with values), and
        'is_complete' (bool).
    """
    missing = []
    populated = []

    for field in REQUIRED_FIELDS:
        value = fields.get(field)
        if value and str(value).strip() and str(value).strip().lower() not in ("null", "none", "n/a", "unknown"):
            populated.append(field)
        else:
            missing.append(field)

    return {
        "missing": missing,
        "populated": populated,
        "is_complete": len(missing) == 0,
    }
