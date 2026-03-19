Overview

An agent that accompliches the following

1. Processes the pdf contract documents in Contracts folder
2. Attempt to extract the following attributes:
    "responseSchema": {
      "type": "object",
      "properties": {
        "audit_date": { "type": "string" },
        "responsible": { "type": "string" },
        "contract_value_per_year": { "type": "string" },
        "category_description": { "type": "string" },
        "gina_account": { "type": "string" },
        "amount_description": { "type": "string" },
        "suppliers": { "type": "string" },
        "supplier_name": { "type": "string" },
        "description_supplier": { "type": "string" },
        "owner_gt": { "type": "string" },
        "department": { "type": "string" },
        "valid_from": { "type": "string" },
        "valid_to": { "type": "string" }
      }
    }
    Based on specific instructions 

    3. Assess whether or not the fields are complete and valid

    4. If not complete the details need to be requested from a person and supplied manually to complete the data.

    5. Finish when the data is complete.