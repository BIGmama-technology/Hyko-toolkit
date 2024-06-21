from hyko_sdk.components.components import RefreshableSelect
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, SupportedProviders
from hyko_sdk.utils import field
from pydantic import BaseModel, ConfigDict

from hyko_toolkit.callbacks_utils.notion_utils import (
    populate_notion_databases,
)
from hyko_toolkit.nodes.writers.notion.insert_database_item.utils import (
    insert_rows_into_notion_database,
    populate_insert_inputs,
)

node = ToolkitNode(
    name="Notion: insert database row",
    description="Insert one row into a notion database.",
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
    database: str = field(
        description="Database to insert into.",
        component=RefreshableSelect(choices=[], callback_id="populate_databases"),
    )
    access_token: str = field(description="oauth access token", hidden=True)


node.callback(trigger="database", id="populate_databases")(populate_notion_databases)
node.callback(trigger="database", id="populate_inputs_from_selected_db")(
    populate_insert_inputs
)


@node.on_call
async def call(inputs: Inputs, params: Params):
    inputs_json = inputs.model_dump()
    res = await insert_rows_into_notion_database(
        database_id=params.database,
        access_token=params.access_token,
        properties=inputs_json,
    )
    return res
