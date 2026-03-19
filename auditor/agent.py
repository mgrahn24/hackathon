from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from .tools.contract_checker import get_contracts_due_for_audit
from .tools.email_sender import send_audit_email

search_agent = LlmAgent(
    name="supplier_researcher",
    model="gemini-2.5-flash",
    description="Searches the web for alternative suppliers given a service description. Returns a plain-text summary of up to 5 alternatives including estimated cost, contract terms, and termination period.",
    instruction="""
You research alternative suppliers for a given service or product.

When given a description of what a current supplier provides, search for up to 5 alternative
suppliers that offer the same or equivalent service. For each alternative gather:
  - Supplier name and website
  - Estimated cost or pricing model (if publicly available)
  - Typical contract terms (e.g. annual, monthly)
  - Typical termination/notice period
  - Any notable strengths or differentiators

Run multiple searches as needed. Search in the same country/region as the current supplier where possible.

Return a formatted plain-text summary like:

  1. Supplier Name (website.com)
     Cost: ~X per month / year
     Terms: Annual contract
     Termination: 3 months notice
     Notes: Market leader in X, SOC2 certified

  2. ...

If pricing is not publicly available, note that and include what is known.
""",
    tools=[google_search],
)

INSTRUCTION = """
You are a contract audit agent. You run daily to check whether any contracts are due for review.

Follow these steps:

1. Call get_contracts_due_for_audit() to retrieve all contracts due today.

2. For each contract returned:

   a. **Research alternatives**: Transfer to the supplier_researcher agent, providing the
      contract's description_supplier, category_description, and supplier_name so it can
      find up to 5 alternative suppliers with cost, terms, and termination details.

   b. **Send email**: Once the research is returned, call send_audit_email() with:
        - to_email: the contract's responsible_email
        - supplier_name: the contract's supplier_name
        - valid_to: the contract's valid_to
        - audit_date: the contract's audit_date
        - source_file: the contract's source_file
        - alternatives_summary: the plain-text summary returned by the researcher

3. Summarise what was done: contracts checked, notifications sent, suppliers researched.

4. If no contracts are due, confirm that all contracts are within their notice period.

Important rules:
- Always research alternatives before sending the email.
- Never modify contract data.
"""

root_agent = LlmAgent(
    name="contract_auditor",
    model="gemini-2.5-flash",
    instruction=INSTRUCTION,
    description="Daily agent that checks contract audit dates, researches alternative suppliers, and emails responsible persons when review is due.",
    tools=[get_contracts_due_for_audit, send_audit_email],
    sub_agents=[search_agent],
)
