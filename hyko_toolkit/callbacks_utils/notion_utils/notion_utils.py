from typing import Any

import httpx
from hyko_sdk.components.components import PortType, Select, SelectChoice
from hyko_sdk.json_schema import Item
from hyko_sdk.models import FieldMetadata, MetaDataBase

from hyko_toolkit.exceptions import APICallError, OauthTokenExpiredError


async def get_notion_databases(access_token: str):
    url = "https://api.notion.com/v1/search"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {"filter": {"property": "object", "value": "database"}}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            databases = response.json().get("results", [])
            return [
                SelectChoice(
                    label=database["title"][0]["text"]["content"], value=database["id"]
                )
                for database in databases
            ]
        if response.status_code == 401:
            raise OauthTokenExpiredError()

        raise APICallError(status=response.status_code, detail=response.text)


async def get_notion_pages(access_token: str):
    url = "https://api.notion.com/v1/search"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {"filter": {"property": "object", "value": "page"}}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            pages = response.json().get("results", [])

            return [
                SelectChoice(
                    label=page["properties"]["title"]["title"][0]["text"]["content"],
                    value=page["id"],
                )
                for page in pages
                if page.get("properties").get("title")
            ]
        if response.status_code == 401:
            raise OauthTokenExpiredError()

        raise APICallError(status=response.status_code, detail=response.text)


async def get_database_columns(database_id: str, access_token: str) -> dict[str, Any]:
    url = f"https://api.notion.com/v1/databases/{database_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            columns = response.json().get("properties", {})
            return columns
        if response.status_code == 401:
            raise OauthTokenExpiredError()

        raise APICallError(status=response.status_code, detail=response.text)


async def populate_notion_databases(
    metadata: MetaDataBase, oauth_token: str, *args: Any
) -> MetaDataBase:
    choices = await get_notion_databases(oauth_token)
    metadata_dict = metadata.params["database"].model_dump()
    metadata_dict["component"] = Select(choices=choices)
    metadata.add_param(FieldMetadata(**metadata_dict))

    return metadata


async def populate_outputs(
    metadata: MetaDataBase, oauth_token: str, *args: Any
) -> MetaDataBase:
    database_id = metadata.params["database"].value
    if database_id:
        columns = await get_database_columns(
            access_token=oauth_token, database_id=database_id
        )

        metadata.outputs = {}
        for column_name, _ in columns.items():
            metadata.add_output(
                FieldMetadata(
                    type=PortType.ARRAY,
                    name=column_name,
                    items=Item(type=PortType.STRING),
                    description=f"Column {column_name}",
                )
            )

    return metadata
