from typing import Any

import httpx
from hyko_sdk.components.components import PortType, Select, SelectChoice, TextField
from hyko_sdk.models import FieldMetadata, MetaDataBase

from hyko_toolkit.callbacks_utils.notion_utils.helpers import get_property_value
from hyko_toolkit.callbacks_utils.notion_utils.notion_utils import get_database_columns
from hyko_toolkit.exceptions import APICallError, OauthTokenExpiredError


async def find_database_items(
    access_token: str, database_id: str, filter: dict[Any, Any]
) -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {
        "filter": filter,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            rows = response.json().get("results", [])
            if len(rows) > 0:
                rows_data: dict[str, Any] = {}
                for key, value in rows[0]["properties"].items():
                    rows_data[key] = [await get_property_value(value)]

                return rows_data
            else:
                return {}

        if response.status_code == 401:
            raise OauthTokenExpiredError()

        raise APICallError(status=response.status_code, detail=response.text)


async def populate_find_inputs(
    metadata: MetaDataBase, oauth_token: str, *args: Any
) -> MetaDataBase:
    database_id = metadata.params["database"].value
    if database_id:
        columns = await get_database_columns(
            access_token=oauth_token, database_id=database_id
        )

        metadata.inputs = {}
        metadata.add_input(
            FieldMetadata(
                type=PortType.STRING,
                name="Column",
                description="Column to filter with.",
                component=Select(
                    choices=[
                        SelectChoice(label=column, value=column)
                        for column in columns.keys()
                    ]
                ),
            ),
        )

        metadata.add_input(
            FieldMetadata(
                type=PortType.STRING,
                name="Value",
                description="Value to search for",
                component=TextField(placeholder="Enter a value"),
            ),
        )

    return metadata
