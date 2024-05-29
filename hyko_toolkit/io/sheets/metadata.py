from typing import Any

import httpx
from hyko_sdk.components.components import PortType, Select
from hyko_sdk.json_schema import Item
from hyko_sdk.models import (
    Category,
    CoreModel,
    FieldMetadata,
    MetaDataBase,
    SupportedProviders,
)
from hyko_sdk.utils import field
from pydantic import TypeAdapter

from hyko_toolkit.exceptions import OauthTokenExpired
from hyko_toolkit.registry import ToolkitNode

input_node = ToolkitNode(
    name="Sheets",
    task="Inputs",
    description="Upload google spreadsheet file.",
    icon="sheets",
    category=Category.IO,
    auth=SupportedProviders.SHEETS,
)


@input_node.set_param
class Param(CoreModel):
    spreadsheet: str = field(
        description="Spreadsheet to read",
        component=Select(choices=[]),
    )
    sheet_name: str = field(
        description="Sheet name",
        component=Select(choices=[]),
    )


@input_node.callback(triggers=["spreadsheet", "sheet_name"], id="update_sheets_node")
async def update_sheets_node(
    metadata: MetaDataBase, oauth_token: str, _
) -> MetaDataBase:
    spreadsheet_id = metadata.params["spreadsheet"].value
    sheet_name = metadata.params["sheet_name"].value

    async with httpx.AsyncClient() as client:
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_name}!1:1"
        response = await client.get(
            url, headers={"Authorization": f"Bearer {oauth_token}"}
        )
    data = response.json()

    if response.status_code == 200:
        data = response.json()
        if "values" in data and len(data["values"]) > 0:
            column_names = data["values"][0]
            for column_name in column_names:
                metadata.add_output(
                    FieldMetadata(
                        type=PortType.ARRAY,
                        name=column_name,
                        items=Item(type=PortType.STRING),
                        description=f"Column {column_name}",
                    )
                )
        async with httpx.AsyncClient() as client:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}"
            response = await client.get(
                url, headers={"Authorization": f"Bearer {oauth_token}"}
            )
        models_adapter = TypeAdapter(dict[str, Any])
        data = models_adapter.validate_json(response.text)
        sheets = data["sheets"]
        choices = [sheet["properties"]["title"] for sheet in sheets]
        metadata_dict = metadata.params["sheet_name"].model_dump()

        metadata_dict["component"] = Select(choices=choices)
        metadata.add_param(FieldMetadata(**metadata_dict))

    elif response.status_code == 401:
        raise OauthTokenExpired
    return metadata
