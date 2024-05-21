from hyko_sdk.models import CoreModel
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from metadata import Inputs, Outputs, func


@func.on_call
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    """Scrapes HTML content from the given URLs and converts it to plain text.

    Args:
        urls (list): A list of URLs to scrape.

    Returns:
        list: A list of transformed documents as plain text.
    """

    loader = AsyncHtmlLoader(web_path=inputs.urls)
    docs = loader.load()
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    # Assuming docs_transformed is a list of transformed documents
    page_contents = []
    # Iterate over each transformed document and concatenate it with the URL header
    for i, text in enumerate(docs_transformed):
        url_header = f"\n=== URL {i+1} {inputs.urls[i]} === \n"
        page_contents.append(f"{url_header}\n{text.page_content}")
    return Outputs(result=page_contents)
