from hyko_sdk.components.components import (
    RefreshableSelect,
    SelectChoice,
)
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import (
    CoreModel,
    FieldMetadata,
    MetaDataBase,
    SupportedProviders,
)
from hyko_sdk.utils import field
from pydantic import PositiveInt

from hyko_toolkit.callbacks_utils.sheets_utils import (
    delete_rows,
    list_sheets_name,
    populate_spreadsheets,
)

func = ToolkitNode(
    name="Delete Rows from sheets",
    description="Delete a row on an existing sheet you have access to.",
    cost=600,
    auth=SupportedProviders.SHEETS,
    icon="sheets",
)


@func.set_input
class Inputs(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    spreadsheet: str = field(
        description="Spreadsheet file to delete from.",
        component=RefreshableSelect(choices=[], callback_id="populate_spreadsheets"),
    )
    sheet: str = field(
        description="Sheet",
        component=RefreshableSelect(choices=[], callback_id="fetch_sheets_delete"),
        hidden=True,
    )
    access_token: str = field(description="oauth access token", hidden=True)
    start_row: PositiveInt = field(description="The row number to start removing from.")
    end_row: PositiveInt = field(description="The row number to end removing by.")


func.callback(trigger="spreadsheet", id="populate_spreadsheets")(populate_spreadsheets)


@func.callback(trigger="spreadsheet", id="fetch_sheets_delete")
async def fetch_sheets_delete(metadata: MetaDataBase, oauth_token: str, _):
    spreadsheet_id = metadata.params["spreadsheet"].value
    if spreadsheet_id:
        sheets = await list_sheets_name(oauth_token, spreadsheet_id)
        choices = [
            SelectChoice(label=sheet.label, value=sheet.value) for sheet in sheets
        ]
        metadata_dict = metadata.params["sheet"].model_dump()
        metadata_dict["component"] = RefreshableSelect(
            choices=choices, callback_id=metadata_dict["component"]["callback_id"]
        )
        metadata_dict["value"] = choices[0].value
        metadata_dict.pop("hidden")
        metadata.add_param(FieldMetadata(**metadata_dict))
    return metadata


@func.on_call
async def call(inputs: Inputs, params: Params):
    res = await delete_rows(
        spreadsheet_id=params.spreadsheet,
        sheet_id=params.sheet,
        access_token=params.access_token,
        start_index=params.start_row - 1,
        end_index=params.end_row - 1,
    )
    return res
