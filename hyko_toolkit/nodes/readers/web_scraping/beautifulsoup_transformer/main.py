import re

import nest_asyncio
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncChromiumLoader

from .metadata import Inputs, Outputs, Params, node


@node.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    """Loads HTML content asynchronously from given URL using Chromium and transforms using BeautifulSoup.

    Args:
        url : URL to load and transform.
        tags_to_extract : List of HTML tags to extract content from.
        attributes_to_extract (list): List of attributes to match in elements.
        strip_tags (bool): Flag indicating whether to strip tags from extracted content.

    Returns:
        string: Extracted content.
    """
    nest_asyncio.apply()
    loader = AsyncChromiumLoader(urls=[inputs.url])
    docs = loader.load()
    soup = BeautifulSoup(str(docs[0]), "html.parser")
    tags = params.tags_to_extract
    attributs = params.attributes_to_extract
    strip = params.strip_tags
    content = ""
    if tags or attributs:
        attrs_dict = {param["name"]: re.compile(param["value"]) for param in attributs}
        elements = soup.find_all(tags, attrs=attrs_dict)
        for e in elements:
            if strip:
                content += e.text.strip()
            else:
                content += str(e)
    else:
        if strip:
            content = " ".join(soup.stripped_strings)

        else:
            content = str(soup)

    return Outputs(result=content)
