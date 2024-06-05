from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .beautifulsoup_transformer.metadata import func as beautifulsoup_transformer_node
from .html2text_transformer.metadata import func as html2text_transformer_node
from .scrapy_crawler.metadata import func as scrapy_crawler_node

node = ToolkitNode(
    name="Web scrapping",
    description="perform various web scraping tasks.",
    tag=Tag.readers,
)


class WebScrapingUtils(str, Enum):
    beautifulsoup_transformer = "beautifulsoup_transformer"
    html2text_transformer = "html2text_transformer"
    scrapy_crawler = "scrapy_crawler"


@node.set_param
class Params(CoreModel):
    web_scraping_util: WebScrapingUtils = field(
        description="Type of the web scraping utility node, when this changes it updates this node",
    )


@node.callback(trigger="web_scraping_util", id="change_web_scraping_util")
async def change_web_scraping_util_type(metadata: MetaDataBase, *_: Any):
    web_scraping_util = metadata.params["web_scraping_util"].value
    metadata.params = {}
    match web_scraping_util:
        case WebScrapingUtils.beautifulsoup_transformer.value:
            return beautifulsoup_transformer_node.get_metadata()
        case WebScrapingUtils.html2text_transformer.value:
            return html2text_transformer_node.get_metadata()
        case WebScrapingUtils.scrapy_crawler.value:
            return scrapy_crawler_node.get_metadata()
        case _:
            return metadata
