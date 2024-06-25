import wikipedia

from .metadata import Inputs, Outputs, Params, node


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Search for articles on Wikipedia based on the given query.

    Args:
    query (str): The search query.
    num_results (int): Number of search results to return (default is 5).
    language (str) : The search Language .
    Returns:
    str: A string containing the concatenated titles and summaries of the search results.
    """
    wikipedia.set_lang(params.language)

    # Perform the Wikipedia search
    search_results = wikipedia.search(inputs.query, results=params.num_results)

    # Retrieve summaries for each search result
    result_str = ""
    for title in search_results:
        try:
            summary = wikipedia.summary(title)
            result_str += f"Title: {title}\nSummary: {summary}\n\n"
        except wikipedia.exceptions.PageError:
            # Handle the case where no summary is available for the article
            pass

    return Outputs(result=result_str)
