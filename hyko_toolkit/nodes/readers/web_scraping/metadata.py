from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .beautifulsoup_transformer.metadata import node as beautifulsoup_transformer_node
from .html2text_transformer.metadata import node as html2text_transformer_node
from .scrapy_crawler.metadata import node as scrapy_crawler_node

node = NodeGroup(
    name="Web scrapping",
    description="perform various web scraping tasks.",
    tag=Tag.readers,
    icon="stack",
    nodes=[
        beautifulsoup_transformer_node,
        html2text_transformer_node,
        scrapy_crawler_node,
    ],
)
