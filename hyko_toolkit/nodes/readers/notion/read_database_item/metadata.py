from hyko_sdk.components.components import RefreshableSelect
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, SupportedProviders
from hyko_sdk.utils import field
from pydantic import BaseModel

from hyko_toolkit.callbacks_utils.notion_utils import (
    populate_notion_databases,
    populate_outputs,
)
from hyko_toolkit.nodes.readers.notion.read_database_item.utils import (
    read_rows_from_notion_database,
)

node = ToolkitNode(
    name="Notion: read database row",
    description="Read one row from a notion database.",
    cost=400,
    auth=SupportedProviders.NOTION,
    icon="notion",
)


class Choices(BaseModel):
    label: str
    value: str


@node.set_input
class Inputs(CoreModel):
    pass


@node.set_param
class Params(CoreModel):
    database: str = field(
        description="Database to read from.",
        component=RefreshableSelect(choices=[], callback_id="populate_databases"),
    )
    access_token: str = field(description="oauth access token", hidden=True)


node.callback(trigger="database", id="populate_databases")(populate_notion_databases)

node.callback(trigger="database", id="populate_outputs_from_selected_dbs")(
    populate_outputs
)


@node.on_call
async def call(inputs: Inputs, params: Params):
    res = await read_rows_from_notion_database(
        database_id=params.database,
        access_token=params.access_token,
    )
    return res
