# src/tools.py

# CHANGE THIS IMPORT: Use langchain_community instead of langchain_tavily
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

@tool
def web_search(query: str):
    """
    Useful for searching the internet for current events, facts, or data.
    """
    # Initialize the tool
    search = TavilySearchResults(max_results=3)
    
    try:
        # Execute search
        # Note: In this version, .invoke() expects a simple string or dict
        results = search.invoke({"query": query})
        
        # Guard against empty results
        if not results:
            return "No results found."

        # Parse results
        # Sometimes results come back as a string, sometimes as a list of dicts
        if isinstance(results, str):
            return results
            
        return "\n".join([
            f"Source: {res.get('url', 'N/A')}\nContent: {res.get('content', 'N/A')}" 
            for res in results
        ])
    except Exception as e:
        return f"Search failed: {str(e)}"

# ... keep your save_report function as is ...
@tool
def save_report(content: str):
    """Saves the final analysis to a markdown file."""
    with open("agent_report.md", "w") as f:
        f.write(content)
    return "Report saved successfully to agent_report.md"