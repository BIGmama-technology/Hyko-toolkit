from hyko_sdk.components.components import RefreshableSelect
from hyko_sdk.models import Category, CoreModel, SupportedProviders
from hyko_sdk.utils import field
from pydantic import BaseModel, ConfigDict

from hyko_toolkit.callbacks_utils.notion_utils.insert_database_row import (
    insert_rows_into_notion_database,
    populate_insert_inputs,
)
from hyko_toolkit.callbacks_utils.notion_utils.shared import populate_notion_databases
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Notion: insert database rows",
    task="Insert rows into notion database",
    description="Insert one or more rows into a notion database.",
    category=Category.API,
    cost=400,
    auth=SupportedProviders.NOTION,
    icon="notion",
)


@func.set_input
class Inputs(CoreModel):
    model_config = ConfigDict(extra="allow")


class Choices(BaseModel):
    label: str
    value: str


@func.set_param
class Params(CoreModel):
    database: str = field(
        description="Database to insert into.",
        component=RefreshableSelect(choices=[], callback_id="populate_databases"),
    )
    access_token: str = field(description="oauth access token", hidden=True)


func.callback(trigger="database", id="populate_databases")(populate_notion_databases)
func.callback(trigger="database", id="populate_inputs_from_selected_db")(
    populate_insert_inputs
)


@func.on_call
async def call(inputs: Inputs, params: Params):
    inputs_json = inputs.model_dump()
    res = await insert_rows_into_notion_database(
        database_id=params.database,
        access_token=params.access_token,
        properties=inputs_json,
    )
    return res
