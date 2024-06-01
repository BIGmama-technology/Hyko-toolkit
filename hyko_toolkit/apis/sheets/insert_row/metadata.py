from typing import Any

from hyko_sdk.components.components import (
    ComplexComponent,
    ListComponent,
    PortType,
    Select,
    SelectChoice,
    SubField,
    TextField,
)
from hyko_sdk.json_schema import Item, Ref
from hyko_sdk.models import (
    Category,
    CoreModel,
    FieldMetadata,
    MetaDataBase,
)
from hyko_sdk.utils import field
from pydantic import BaseModel, ConfigDict

from hyko_toolkit.apis.sheets.common import (
    Dimension,
    get_sheet_columns,
    get_spreadsheets,
    insert_google_sheet_values,
    list_sheets_name,
)
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Insert rows to sheets",
    task="Insert rows to sheets",
    description="Add one or more new rows in a specific spreadsheet.",
    category=Category.API,
    cost=600,
)


@func.set_input
class Inputs(CoreModel):
    model_config = ConfigDict(extra="allow")


class Choices(BaseModel):
    label: str
    value: str


@func.set_param
class Params(CoreModel):
    spreadsheet: str = field(
        description="Spreadsheet file to append to.",
        component=Select(choices=[]),
    )
    sheet: str = field(
        description="Sheet",
        component=Select(choices=[]),
    )
    access_token: str = field(description="oauth access token")


@func.callback(
    triggers=["spreadsheet"], id="populate_spreadsheets_insert", is_refresh=True
)
async def populate_spreadsheets_insert(
    metadata: MetaDataBase, oauth_token: str, *args: Any
) -> MetaDataBase:
    choices = await get_spreadsheets(str(metadata.params["access_token"].value))
    metadata_dict = metadata.params["spreadsheet"].model_dump()
    metadata_dict["component"] = Select(choices=choices)
    metadata.add_param(FieldMetadata(**metadata_dict))

    return metadata


@func.callback(triggers=["sheet"], id="populate_sheets_insert", is_refresh=True)
async def populate_sheets_insert(
    metadata: MetaDataBase, oauth_token: str, *args: Any
) -> MetaDataBase:
    choices = await list_sheets_name(
        str(metadata.params["access_token"].value),
        str(metadata.params["spreadsheet"].value),
    )
    metadata_dict = metadata.params["sheet"].model_dump()
    metadata_dict["component"] = Select(
        choices=[
            SelectChoice(value=choice.label, label=choice.label) for choice in choices
        ]
    )
    metadata.add_param(FieldMetadata(**metadata_dict))
    return metadata


@func.callback(triggers=["spreadsheet"], id="fetch_sheets")
async def fetch_sheets(metadata: MetaDataBase, oauth_token: str, _):
    spreadsheet_id = metadata.params["spreadsheet"].value
    if spreadsheet_id:
        sheets = await list_sheets_name(
            str(metadata.params["access_token"].value), spreadsheet_id
        )

        choices = [
            SelectChoice(label=sheet.label, value=sheet.label) for sheet in sheets
        ]
        metadata_dict = metadata.params["sheet"].model_dump()
        metadata_dict["component"] = Select(choices=choices)
        metadata.params["sheet"].value = {}
        metadata.inputs = {}
        metadata.add_param(FieldMetadata(**metadata_dict))
        return metadata
    return metadata


@func.callback(triggers=["sheet"], id="add_sheet_insert_rows_inputs")
async def add_sheet_insert_rows_values(
    metadata: MetaDataBase, oauth_token: str, _
) -> MetaDataBase:
    spreadsheet_id = metadata.params["spreadsheet"].value
    sheet_name = metadata.params["sheet"].value
    if spreadsheet_id and sheet_name:
        columns = await get_sheet_columns(
            str(metadata.params["access_token"].value), spreadsheet_id, sheet_name
        )
        metadata.inputs = {}
        if len(columns) > 0:
            a = {"$ref": "test"}
            metadata.add_input(
                FieldMetadata(
                    type=PortType.ARRAY,
                    name="values",
                    description="Column names",
                    items=Ref(**a),
                    component=ListComponent(
                        item_component=ComplexComponent(
                            fields=[
                                SubField(
                                    type="string",
                                    name=column,
                                    description="",
                                    component=TextField(placeholder="Enter a value"),
                                )
                                for column in columns
                            ]
                        )
                    ),
                )
            )
        else:
            metadata.inputs = {}
            metadata.add_input(
                FieldMetadata(
                    type=PortType.ARRAY,
                    name="values",
                    items=Item(type=PortType.STRING),
                    description="",
                    component=ListComponent(
                        item_component=ListComponent(
                            item_component=TextField(placeholder="Enter a value")
                        )
                    ),
                )
            )
    return metadata


@func.on_call
async def call(inputs: Inputs, params: Params):
    inputs_json = inputs.model_dump()
    if isinstance(inputs_json["values"][0], dict):
        values = [[d[key] for key in d] for d in inputs_json["values"]]
    else:
        values = inputs_json["values"]
    res = await insert_google_sheet_values(
        access_token=params.access_token,
        spreadsheet_id=params.spreadsheet,
        sheet_name=params.sheet,
        values=values,
        dimension=Dimension.ROWS,
    )
    return res
