REQUIRED_FIELDS = [
    "audit_date",
    "responsible",
    "contract_value_per_year",
    "category_description",
    "gina_account",
    "amount_description",
    "suppliers",
    "supplier_name",
    "description_supplier",
    "owner_gt",
    "department",
    "valid_from",
    "valid_to",
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
