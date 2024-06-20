import logging

from hyko_sdk.components.components import RefreshableSelect
from hyko_sdk.models import Category, CoreModel, SupportedProviders
from hyko_sdk.utils import field
from pydantic import BaseModel

from hyko_toolkit.callbacks_utils.notion_utils.find_database_item import (
    find_database_items,
    populate_find_inputs,
)
from hyko_toolkit.callbacks_utils.notion_utils.notion_utils import (
    populate_notion_databases,
)
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Notion: Find a database row ",
    task="Find a row in a notion database",
    description="Find a row in a notion database",
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
        description="Database to search in.",
        component=RefreshableSelect(choices=[], callback_id="populate_databases"),
    )
    access_token: str = field(description="oauth access token", hidden=True)


func.callback(trigger="database", id="populate_databases")(populate_notion_databases)

func.callback(trigger="database", id="populate_inputs_from_selected_db")(
    populate_find_inputs
)


@func.on_call
async def call(inputs: Inputs, params: Params):
    logging.warning(inputs)
    res = await find_database_items(
        database_id=params.database,
        access_token=params.access_token,
        filter={property: "Category", "select": {"equal": "Project"}},
    )
    return res
