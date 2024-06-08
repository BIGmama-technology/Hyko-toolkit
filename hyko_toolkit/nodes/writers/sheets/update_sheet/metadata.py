from typing import Any

from hyko_sdk.components.components import (
    ButtonComponent,
    PortType,
    RefreshableSelect,
    SelectChoice,
    TextField,
)
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import (
    CoreModel,
    FieldMetadata,
    MetaDataBase,
    SupportedProviders,
)
from hyko_sdk.utils import field
from pydantic import ConfigDict

from hyko_toolkit.callbacks_utils.sheets_utils import (
    Response,
    get_sheet_columns,
    list_sheets_name,
    populate_sheets,
    populate_spreadsheets,
    update_google_sheet_row,
)

node = ToolkitNode(
    name="Update Row",
    description="Overwrite values in an existing row.",
    cost=600,
    auth=SupportedProviders.SHEETS,
    icon="sheets",
)


@node.set_input
class Inputs(CoreModel):
    model_config = ConfigDict(extra="allow")


@node.set_param
class Params(CoreModel):
    spreadsheet: str = field(
        description="Spreadsheet file to update.",
        component=RefreshableSelect(choices=[], callback_id="populate_spreadsheets"),
    )
    sheet: str = field(
        description="Sheet",
        component=RefreshableSelect(choices=[], callback_id="populate_sheets_insert"),
        hidden=True,
    )
    access_token: str = field(description="oauth access token", hidden=True)
    values: str = field(description="Values passed to update the row", hidden=True)
    row_number: int = field(description="The row number to update", hidden=True)
    add_column: str = field(
        description="Add new column",
        component=ButtonComponent(text="Add new column"),
        hidden=True,
    )


node.callback(trigger="spreadsheet", id="populate_spreadsheets")(populate_spreadsheets)


node.callback(trigger="sheet", id="populate_sheets_insert")(populate_sheets)


@node.callback(trigger="sheet", id="add_sheet_update_rows_inputs")
async def add_sheet_update_row_values(
    metadata: MetaDataBase, oauth_token: str, _
) -> MetaDataBase:
    spreadsheet_id = metadata.params["spreadsheet"].value
    sheet_name = metadata.params["sheet"].value
    if spreadsheet_id and sheet_name:
        columns = await get_sheet_columns(oauth_token, spreadsheet_id, sheet_name)
        metadata.inputs = {}
        if len(columns) > 0:
            for column in columns:
                metadata.add_input(
                    FieldMetadata(
                        type=PortType.STRING,
                        name=column,
                        description=column,
                        component=TextField(placeholder="Enter a value"),
                        value="",
                    ),
                )
            if "add_column" in metadata.params:
                metadata.params.pop("add_column")
        else:
            metadata.inputs = {}
            metadata.add_input(
                FieldMetadata(
                    type=PortType.STRING,
                    name="column_1",
                    description="",
                    component=TextField(placeholder="Enter a value"),
                    value="",
                )
            )
            metadata.add_param(
                FieldMetadata(
                    type=PortType.ANY,
                    name="add_column",
                    description="Add new column",
                    component=ButtonComponent(text="Add new column"),
                    callback_id="add_new_input_column",
                )
            )
    return metadata


@node.callback(trigger="add_column", id="add_new_input_column")
async def add_new_input_column(metadata: MetaDataBase, *_: Any):
    metadata.add_input(
        FieldMetadata(
            type=PortType.STRING,
            name=f"column_{len(metadata.inputs.keys()) + 1}",
            description="",
            component=TextField(placeholder="Enter a value"),
            value="",
        )
    )

    return metadata


@node.callback(trigger="spreadsheet", id="fetch_sheets_update")
async def fetch_sheets_update(metadata: MetaDataBase, oauth_token: str, _):
    spreadsheet_id = metadata.params["spreadsheet"].value
    if spreadsheet_id:
        sheets = await list_sheets_name(oauth_token, spreadsheet_id)
        choices = [
            SelectChoice(label=sheet.label, value=sheet.label) for sheet in sheets
        ]
        metadata_dict = metadata.params["sheet"].model_dump()
        metadata_dict["component"] = RefreshableSelect(
            choices=choices, callback_id=metadata_dict["component"]["callback_id"]
        )
        metadata_dict["value"] = choices[0].value
        metadata_dict.pop("hidden")
        metadata.add_param(FieldMetadata(**metadata_dict))
        metadata_dict = metadata.params["row_number"].model_dump()
        metadata_dict.pop("hidden")
        metadata.add_param(FieldMetadata(**metadata_dict))
        metadata = await add_sheet_update_row_values(metadata, oauth_token, _)

    return metadata


@node.on_call
async def call(inputs: Inputs, params: Params):
    inputs_json = inputs.model_dump()
    values = [inputs_json[key] for key in inputs_json]

    res = await update_google_sheet_row(
        access_token=params.access_token,
        spreadsheet_id=params.spreadsheet,
        sheet_name=params.sheet,
        values=values,
        row_index=params.row_number,
    )
    return Response(success=True, body=str(res.body))
