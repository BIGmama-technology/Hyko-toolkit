from typing import Any

import httpx
from hyko_sdk.components.components import RefreshableSelect, SelectChoice
from hyko_sdk.models import FieldMetadata, MetaDataBase

from hyko_toolkit.callbacks_utils.sheets_utils import Body, CreateResponse, Response
from hyko_toolkit.exceptions import APICallError, OauthTokenExpiredError

base_url = "https://docs.googleapis.com/v1"


async def populate_documents(
    metadata: MetaDataBase, oauth_token: str, *_: Any
) -> MetaDataBase:
    choices = await get_docs(oauth_token)
    metadata_dict = metadata.params["document"].model_dump()
    metadata_dict["component"] = RefreshableSelect(
        choices=choices, callback_id=metadata_dict["component"]["callback_id"]
    )
    metadata.add_param(FieldMetadata(**metadata_dict))
    return metadata


async def create_document(title: str, access_token: str):
    url = f"{base_url}/documents"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    json_body = {
        "title": title,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json_body)
        if response.status_code == 200:
            return CreateResponse(
                success=response.is_success, body=Body(**response.json())
            )
        if response.status_code == 401:
            raise OauthTokenExpiredError()
        raise APICallError(status=response.status_code, detail=response.text)


async def read_from_document(document_id: str, access_token: str):
    url = f"{base_url}/documents/{document_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers)
        if response.status_code == 200:
            document = response.json()

            document_text = ""
            for element in document["body"]["content"]:
                if "paragraph" in element:
                    for paragraph_element in element["paragraph"]["elements"]:
                        if "textRun" in paragraph_element:
                            document_text += paragraph_element["textRun"]["content"]
            return document_text
        if response.status_code == 401:
            raise OauthTokenExpiredError()
        raise APICallError(status=response.status_code, detail=response.text)


async def write_to_document(document_id: str, body: str, access_token: str):
    url = f"{base_url}/documents/{document_id}:batchUpdate"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    json_body: dict[str, Any] = {
        "requests": [
            {
                "insertText": {
                    "text": body,
                    "endOfSegmentLocation": {},
                },
            },
        ],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json_body)
        if response.status_code == 200:
            return Response(success=response.is_success, body=response.text)
        if response.status_code == 401:
            raise OauthTokenExpiredError()
        raise APICallError(status=response.status_code, detail=response.text)


async def get_docs(access_token: str):
    url = "https://www.googleapis.com/drive/v3/files"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    queries = ["mimeType='application/vnd.google-apps.document'", "trashed=false"]
    params = {
        "q": " and ".join(queries),
        "includeItemsFromAllDrives": "true",
        "supportsAllDrives": "true",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            docs = response.json().get("files", [])
            return [SelectChoice(label=doc["name"], value=doc["id"]) for doc in docs]
        if response.status_code == 401:
            raise OauthTokenExpiredError()
        raise APICallError(status=response.status_code, detail=response.text)
