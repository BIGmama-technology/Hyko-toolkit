from hyko_sdk.components.components import RefreshableSelect
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, SupportedProviders
from hyko_sdk.utils import field
from pydantic import BaseModel, ConfigDict

from hyko_toolkit.nodes.writers.notion.append_to_page.utils import (
    append_block_to_page,
    populate_append_input,
    populate_notion_pages,
)

node = ToolkitNode(
    name="Notion: append to a page ",
    description="Append markdown content to a notion page",
    cost=400,
    auth=SupportedProviders.NOTION,
    icon="notion",
)


@node.set_input
class Inputs(CoreModel):
    model_config = ConfigDict(extra="allow")


class Choices(BaseModel):
    label: str
    value: str


@node.set_param
class Params(CoreModel):
    page: str = field(
        description="Page to append to it",
        component=RefreshableSelect(choices=[], callback_id="populate_pages"),
    )
    access_token: str = field(description="oauth access token", hidden=True)


node.callback(trigger="page", id="populate_pages")(populate_notion_pages)

node.callback(trigger="page", id="populate_input")(populate_append_input)


@node.on_call
async def call(inputs: Inputs, params: Params):
    res = await append_block_to_page(
        access_token=params.access_token,
        markdown_content=str(inputs.model_dump()["Content"]),
        page_id=params.page,
    )
    return res
