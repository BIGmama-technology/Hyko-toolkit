from enum import Enum

import httpx
from pydantic import BaseModel

from hyko_toolkit.exceptions import APICallError


class Dimension(Enum):
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"


class Response(BaseModel):
    success: bool
    body: str


async def get_spreadsheets(access_token: str):
    url = "https://www.googleapis.com/drive/v3/files"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    queries = ["mimeType='application/vnd.google-apps.spreadsheet'", "trashed=false"]
    params = {
        "q": " and ".join(queries),
        "includeItemsFromAllDrives": "true",
        "supportsAllDrives": "true",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        # raise exception forerrors
        data = response.json()
        spreadsheets = data["files"]
        return [
            {"label": sheet["name"], "value": sheet["id"]} for sheet in spreadsheets
        ]


async def list_sheets_name(access_token: str, spreadsheet_id: str):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        # handle error
        sheets = response.json().get("sheets", [])
    return [
        {"label": sheet["properties"]["title"], "value": sheet["properties"]["sheetId"]}
        for sheet in sheets
    ]


async def delete_rows(
    spreadsheet_id: str,
    sheet_id: int,
    start_index: int,
    end_index: int,
    access_token: str,
):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    body = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": Dimension.ROWS,
                        "startIndex": start_index,
                        "endIndex": end_index,
                    }
                }
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        return Response(success=response.is_success, body=response.text)


async def insert_google_sheet_values(
    access_token: str,
    spreadsheet_id: str,
    sheet_name: str,
    values: list[list[str]],
    dimension: Dimension,
):
    request_body = {
        "majorDimension": dimension.value,
        "range": f"{sheet_name}!A:A",
        "values": [{"values": val} for val in values],
    }
    print("request body", request_body)

    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_name}!A:A:append"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    query_params = {
        "valueInputOption": "USER_ENTERED",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers=headers, json=request_body, params=query_params
        )
    if response.is_success:
        return Response(success=response.is_success, body=response.text)
    else:
        raise APICallError(status=response.status_code, detail=response.text)
