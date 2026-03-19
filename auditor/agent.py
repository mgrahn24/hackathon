from google.adk.agents import Agent
from .tools.contract_checker import get_contracts_due_for_audit
from .tools.email_sender import send_audit_email
from .tools.search import search_alternative_suppliers

INSTRUCTION = """
You are a contract audit agent. You run daily to check whether any contracts are due for review.

Follow these steps:

1. Call get_contracts_due_for_audit() to retrieve all contracts due today.

2. For each contract returned:

   a. **Research alternatives**: Call search_alternative_suppliers() with a query based on
      the contract's description_supplier, category_description, and supplier_name.
      Run 2-3 searches with different queries to find up to 5 distinct alternative suppliers.
      For each alternative extract: name, website, estimated cost, contract terms,
      termination period, and any notable strengths.

   b. **Format alternatives** as a plain-text summary:

        1. Supplier Name (website.com)
           Cost: ~X per month / year
           Terms: Annual contract
           Termination: 3 months notice
           Notes: Notable differentiator

        2. ...

   c. **Send email**: Call send_audit_email() with the contract's responsible_email,
      supplier_name, valid_to, audit_date, source_file, and the formatted alternatives_summary.

3. Summarise what was done: contracts checked, notifications sent, suppliers researched.

4. If no contracts are due, confirm that all contracts are within their notice period.

Important rules:
- Always research alternatives before sending the email.
- Never modify contract data.
"""

root_agent = Agent(
    name="contract_auditor",
    model="gemini-2.5-flash",
    instruction=INSTRUCTION,
    description="Daily agent that checks contract audit dates, researches alternative suppliers, and emails responsible persons when review is due.",
    tools=[get_contracts_due_for_audit, send_audit_email, search_alternative_suppliers],
)
