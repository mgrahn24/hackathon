import logging
from duckduckgo_search import DDGS

log = logging.getLogger(__name__)


def search_alternative_suppliers(query: str) -> str:
    """Searches the web for alternative suppliers or services using DuckDuckGo.

    Args:
        query: A search query describing the service or product to find alternatives for.

    Returns:
        A plain-text list of up to 5 search results with title, URL, and snippet.
    """
    log.info("Searching for: %s", query)
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No results found."
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r['title']}\n   {r['href']}\n   {r['body']}")
        return "\n\n".join(lines)
    except Exception as e:
        log.error("Search failed: %s", e)
        return f"Search failed: {e}"
