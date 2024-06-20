from typing import Any

import httpx

from hyko_toolkit.callbacks_utils.notion_utils.helpers import get_property_value
from hyko_toolkit.exceptions import APICallError, OauthTokenExpiredError


async def read_rows_from_notion_database(
    database_id: str, access_token: str
) -> dict[str, Any]:
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {"page_size": 1}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
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
