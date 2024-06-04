from enum import Enum
from typing import Any

import httpx
from hyko_sdk.components.components import Select, SelectChoice
from hyko_sdk.models import FieldMetadata, MetaDataBase
from pydantic import BaseModel

from hyko_toolkit.exceptions import APICallError, OauthTokenExpiredError


class Dimension(Enum):
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"


class Response(BaseModel):
    success: bool
    body: str


async def populate_spreadsheets(
    metadata: MetaDataBase, oauth_token: str, *_: Any
) -> MetaDataBase:
    choices = await get_spreadsheets(oauth_token)
    metadata_dict = metadata.params["spreadsheet"].model_dump()
    metadata_dict["component"] = Select(choices=choices)
    metadata.add_param(FieldMetadata(**metadata_dict))

    return metadata


async def populate_sheets(
    metadata: MetaDataBase, oauth_token: str, *_: Any
) -> MetaDataBase:
    spreadsheet_id = metadata.params["spreadsheet"].value
    if spreadsheet_id:
        choices = await list_sheets_name(
            oauth_token, str(metadata.params["spreadsheet"].value)
        )
        metadata_dict = metadata.params["sheet"].model_dump()
        metadata_dict["component"] = Select(
            choices=[
                SelectChoice(value=choice.label, label=choice.label)
                for choice in choices
            ]
        )
        metadata.add_param(FieldMetadata(**metadata_dict))
    return metadata


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
        if response.status_code == 200:
            spreadsheets = response.json().get("files", [])
            return [
                SelectChoice(label=spreadsheet["name"], value=spreadsheet["id"])
                for spreadsheet in spreadsheets
            ]
        if response.status_code == 401:
            raise OauthTokenExpiredError()
        raise APICallError(status=response.status_code, detail=response.text)


async def list_sheets_name(access_token: str, spreadsheet_id: str):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            sheets = response.json().get("sheets", [])
            return [
                SelectChoice(
                    label=sheet["properties"]["title"],
                    value=sheet["properties"]["sheetId"],
                )
                for sheet in sheets
            ]
        elif response.status_code == 401:
            raise OauthTokenExpiredError()
        raise APICallError(status=response.status_code, detail=response.text)


async def get_sheet_columns(
    access_token: str, spreadsheet_id: str, sheet_name: str
) -> list[str]:
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_name}!1:1"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "values" in data and len(data["values"]) > 0:
                return data["values"][0]
            else:
                return []
        elif response.status_code == 401:
            raise OauthTokenExpiredError()
        raise APICallError(status=response.status_code, detail=response.text)


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


async def clear_sheet(
    spreadsheet_id: str,
    sheet_id: int,
    access_token: str,
    row_index: int,
    num_of_rows: int,
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
                        "dimension": "ROWS",
                        "startIndex": row_index,
                        "endIndex": row_index + num_of_rows + 1,
                    },
                },
            },
        ],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        return Response(success=response.is_success, body=response.text)
