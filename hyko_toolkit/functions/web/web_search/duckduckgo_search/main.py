from duckduckgo_search import DDGS
from metadata import Inputs, Outputs, Params, func


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Search the web using DuckDuckGo and return all results as a single string.

    Args:
    query (str): The search query.
    max_results (int): Maximum number of search results to return (default is 5).

    Returns:
    str: A single string containing all search results.
    """
    # Initialize DuckDuckGo search session
    with DDGS() as ddgs:
        # Perform the search and retrieve results
        results = list(ddgs.text(inputs.query, max_results=params.max_results))  # type: ignore
        # Concatenate titles and URLs into a single strings
        result_str = ""
        for result in results:
            result_str += f"Title: {result['title']}\nURL: {result['href']}\nBody: {result['body']}\n\n"

    return Outputs(result=result_str)
