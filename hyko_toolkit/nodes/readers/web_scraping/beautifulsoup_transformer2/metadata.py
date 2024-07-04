import nest_asyncio
from hyko_sdk.components.components import ListComponent, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers.beautiful_soup_transformer import (
    BeautifulSoupTransformer,
)

node = ToolkitNode(
    name="Beautifulsoup transformer2",
    cost=5,
    description="Scrape HTML content from URLs and convert it to plain text",
)


@node.set_input
class Inputs(CoreModel):
    urls: list[str] = field(
        description="A list of URLs to scrape. Protocol must be either 'http' or 'https'.",
        component=ListComponent(item_component=TextField(placeholder="Enter URL")),
    )


@node.set_param
class Params(CoreModel):
    tags_to_extract: str = field(
        description="Specify HTML tags for extraction, separated by commas."
    )


@node.set_output
class Outputs(CoreModel):
    result: list[str] = field(
        description="List of transformed documents as plain text."
    )


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
    nest_asyncio.apply()  # type: ignore
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
        page_contents.append(f"{url_header}\n{text.page_content}")  # type: ignore
    return Outputs(result=page_contents)  # type: ignore
