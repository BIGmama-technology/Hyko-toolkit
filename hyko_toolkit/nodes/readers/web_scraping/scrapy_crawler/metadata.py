from hyko_sdk.components.components import ListComponent, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="Scrapy crawler",
    cost=5,
    description="use scrapy to crawl web pages",
)


@func.set_input
class Inputs(CoreModel):
    start_url: list[str] = field(
        description="A starting url to crawl. Protocol must be either 'http' or 'https'.",
        component=ListComponent(
            item_component=TextField(placeholder="http://example.com/example1.html")
        ),
    )
    stop_url: list[str] = field(
        description="A list of urls to stop crawling. Protocol must be either 'http' or 'https'.",
        component=ListComponent(
            item_component=TextField(placeholder="http://example.com/example2.html")
        ),
    )


@func.set_param
class Params(CoreModel):
    allowed_domain: list[str] = field(
        description="A domain to crawl.",
        component=ListComponent(item_component=TextField(placeholder="example.com")),
    )


@func.set_output
class Outputs(CoreModel):
    urls: list[str] = field(description="A list of crawled urls.")
    text: list[str] = field(description="A list of crawled text.")
