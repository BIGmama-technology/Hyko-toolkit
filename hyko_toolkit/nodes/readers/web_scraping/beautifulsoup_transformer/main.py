import nest_asyncio
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

from .metadata import Inputs, Outputs, Params, node


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    """Loads HTML content asynchronously from given URLs using Chromium and transforms using BeautifulSoup.

    Args:
        urls (list): A list of URLs to load and transform.
        tags_to_extract (list, optional): A list of HTML tags to extract content from.
            Defaults to ["span"].

    Returns:
        list: A list of transformed documents with content from specified tags.
    """
    nest_asyncio.apply()
    loader = AsyncChromiumLoader(urls=inputs.urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    tags = "".join(params.tags_to_extract.split()).split(",")
    docs_transformed = bs_transformer.transform_documents(docs, tags)
    # Assuming docs_transformed is a list of transformed documents
    page_contents = []
    # Iterate over each transformed document and concatenate it with the URL header
    for i, text in enumerate(docs_transformed):
        url_header = f"\n=== URL {i+1} {inputs.urls[i]} === \n"
        page_contents.append(f"{url_header}\n{text.page_content}")
    return Outputs(result=page_contents)
