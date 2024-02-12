from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
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
    page_contents = [text.page_content for text in docs_transformed]

    return Outputs(result=page_contents)
