import nest_asyncio
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from metadata import Inputs, Outputs, Params, func


@func.on_execute
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
    tags = params.tags_to_extract.split("+")
    docs_transformed = bs_transformer.transform_documents(docs, tags)
    page_contents = [text.page_content for text in docs_transformed]
    return Outputs(result=page_contents)
