from hyko_sdk.components.components import RefreshableSelect
from hyko_sdk.models import Category, CoreModel, SupportedProviders
from hyko_sdk.utils import field
from pydantic import BaseModel

from hyko_toolkit.callbacks_utils.notion_utils.notion_utils import (
    populate_notion_databases,
    populate_outputs,
)
from hyko_toolkit.callbacks_utils.notion_utils.read_database_row import (
    read_rows_from_notion_database,
)
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Notion: read database row",
    task="Read a row from notion database",
    description="Read one row from a notion database.",
    category=Category.API,
    cost=400,
    auth=SupportedProviders.NOTION,
    icon="notion",
)


class Choices(BaseModel):
    label: str
    value: str


@func.set_input
class Inputs(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    database: str = field(
        description="Database to read from.",
        component=RefreshableSelect(choices=[], callback_id="populate_databases"),
    )
    access_token: str = field(description="oauth access token", hidden=True)


func.callback(trigger="database", id="populate_databases")(populate_notion_databases)

func.callback(trigger="database", id="populate_outputs_from_selected_dbs")(
    populate_outputs
)


@func.on_call
async def call(inputs: Inputs, params: Params):
    res = await read_rows_from_notion_database(
        database_id=params.database,
        access_token=params.access_token,
    )
    return res
