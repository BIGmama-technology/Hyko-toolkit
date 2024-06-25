from typing import Any

import httpx
from hyko_sdk.components.components import (
    PortType,
    RefreshableSelect,
    SelectChoice,
)
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
                    label=database["title"][0]["text"]["content"]
                    if len(database["title"]) > 0
                    else "Untitled database",
                    value=database["id"],
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
                    label=page["properties"]["title"]["title"][0]["text"]["content"]
                    if len(page["properties"]["title"]["title"]) > 0
                    else "Untitled page",
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
    metadata_dict["component"] = RefreshableSelect(
        choices=choices, callback_id="populate_databases"
    )
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
                    type=PortType.STRING,
                    name=column_name,
                    description=f"Column {column_name}",
                )
            )

    return metadata


async def get_property_structure(type: str, value: str):  # noqa: C901
    if type == "title":
        return {type: [{"text": {"content": value}}]}
    elif type == "status":
        return {type: {"name": value}}
    elif type == "url":
        return {type: value}
    elif type == "phone_number":
        return {type: value}
    elif type == "number":
        return {type: int(value)}
    elif type == "checkbox":
        return {type: value}
    elif type == "date":
        return {type: {"start": value}}
    elif type == "email":
        return {type: value}
    elif type == "multi_select":
        return {type: [{"name": value}]}
    elif type == "select":
        return {type: {"name": value}}


async def get_property_value(property: dict[str, Any]):  # noqa: C901
    if property["type"] == "title":
        return property["title"][0]["text"]["content"]
    elif property["type"] == "status":
        return property["status"]["name"]
    elif property["type"] == "url":
        return property["url"]
    elif property["type"] == "phone_number":
        return property["url"]
    elif property["type"] == "number":
        return int(property["number"])
    elif property["type"] == "checkbox":
        return property["checkbox"]
    elif property["type"] == "date":
        return property["date"]["start"]
    elif property["type"] == "email":
        return property["email"]
    elif property["type"] == "multi_select":
        return property["multi_select"][0]["name"]
    elif property["type"] == "select":
        return property["select"]["name"]
