from typing import Any

import httpx
from hyko_sdk.components.components import (
    PortType,
    Select,
    SelectChoice,
    TextField,
    Toggle,
)
from hyko_sdk.models import FieldMetadata, MetaDataBase
from pydantic import BaseModel

from hyko_toolkit.callbacks_utils.notion_utils.helpers import get_property_structure
from hyko_toolkit.callbacks_utils.notion_utils.notion_utils import get_database_columns
from hyko_toolkit.exceptions import APICallError, OauthTokenExpiredError


class SuccessInsertionResponse(BaseModel):
    success: bool


async def populate_insert_inputs(
    metadata: MetaDataBase, oauth_token: str, *args: Any
) -> MetaDataBase:
    database_id = metadata.params["database"].value
    if database_id:
        columns = await get_database_columns(
            access_token=oauth_token, database_id=database_id
        )

        metadata.inputs = {}
        component = None
        for column_name, column_properties in columns.items():
            if column_properties["type"] == "checkbox":
                component = Toggle()
            elif column_properties["type"] == "multi_select":
                component = Select(
                    choices=[
                        SelectChoice(label=option["name"], value=option["name"])
                        for option in column_properties["multi_select"]["options"]
                    ]
                )

            elif column_properties["type"] == "select":
                component = Select(
                    choices=[
                        SelectChoice(label=option["name"], value=option["name"])
                        for option in column_properties["select"]["options"]
                    ]
                )

            elif column_properties["type"] == "status":
                component = Select(
                    choices=[
                        SelectChoice(label=option["name"], value=option["name"])
                        for option in column_properties["status"]["options"]
                    ]
                )

            else:
                component = TextField(placeholder="Enter a value")

            metadata.add_input(
                FieldMetadata(
                    type=PortType.STRING,
                    name=column_name,
                    description=f"Column {column_name}",
                    component=component,
                ),
            )

    return metadata


async def insert_rows_into_notion_database(
    database_id: str, properties: dict[Any, Any], access_token: str
) -> SuccessInsertionResponse:
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    columns = await get_database_columns(
        database_id=database_id, access_token=access_token
    )

    typed_columns: dict[str, str] = {}
    for key, value in columns.items():
        typed_columns[key] = value["type"]

    rows: dict[str, Any] = {}
    for key, value in properties.items():
        structure = await get_property_structure(type=typed_columns[key], value=value)
        rows[key] = structure

    data = {
        "parent": {"type": "database_id", "database_id": database_id},
        "properties": rows,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return SuccessInsertionResponse(success=True)
        if response.status_code == 401:
            raise OauthTokenExpiredError()

        raise APICallError(status=response.status_code, detail=response.text)
