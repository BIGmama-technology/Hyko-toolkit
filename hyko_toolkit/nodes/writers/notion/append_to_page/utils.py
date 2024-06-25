from typing import Any

import httpx
from hyko_sdk.components.components import (
    PortType,
    RefreshableSelect,
    TextField,
)
from hyko_sdk.models import FieldMetadata, MetaDataBase
from pydantic import BaseModel

from hyko_toolkit.callbacks_utils.notion_utils import (
    get_notion_pages,
)
from hyko_toolkit.exceptions import APICallError, OauthTokenExpiredError


class SuccessAppendResponse(BaseModel):
    success: bool


async def append_block_to_page(access_token: str, markdown_content: str, page_id: str):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": markdown_content}}
                    ]
                },
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            return SuccessAppendResponse(success=True)
        if response.status_code == 401:
            raise OauthTokenExpiredError()

        raise APICallError(status=response.status_code, detail=response.text)


async def populate_notion_pages(
    metadata: MetaDataBase, oauth_token: str, *args: Any
) -> MetaDataBase:
    choices = await get_notion_pages(oauth_token)
    metadata_dict = metadata.params["page"].model_dump()
    metadata_dict["component"] = RefreshableSelect(
        choices=choices, callback_id="populate_pages"
    )
    metadata.add_param(FieldMetadata(**metadata_dict))

    return metadata


async def populate_append_input(
    metadata: MetaDataBase, oauth_token: str, *args: Any
) -> MetaDataBase:
    metadata.inputs = {}
    metadata.add_input(
        FieldMetadata(
            type=PortType.STRING,
            name="Content",
            description="Content to be appended to the page",
            component=TextField(placeholder="Enter a value"),
        ),
    )

    return metadata
