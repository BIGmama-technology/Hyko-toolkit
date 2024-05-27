import httpx


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
                        "dimension": "ROWS",
                        "startIndex": start_index,
                        "endIndex": end_index,
                    }
                }
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        # raise an exception for errors
        return response.json()
