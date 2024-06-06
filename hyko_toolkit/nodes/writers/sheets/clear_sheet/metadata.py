from hyko_sdk.components.components import (
    RefreshableSelect,
    Select,
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

from hyko_toolkit.callbacks_utils.sheets_utils import (
    Response,
    delete_rows,
    get_values,
    list_sheets_name,
    populate_spreadsheets,
)

node = ToolkitNode(
    name="Clear Sheet",
    description="Clears all rows on an existing sheet.",
    cost=600,
    auth=SupportedProviders.SHEETS,
    icon="sheets",
)


@node.set_input
class Inputs(CoreModel):
    pass


@node.set_param
class Params(CoreModel):
    spreadsheet: str = field(
        description="Spreadsheet file to clear.",
        component=RefreshableSelect(choices=[], callback_id="populate_spreadsheets"),
    )
    sheet: str = field(
        description="Sheet",
        component=RefreshableSelect(choices=[], callback_id="fetch_sheets_delete"),
        hidden=True,
    )
    access_token: str = field(description="oauth access token", hidden=True)


node.callback(trigger="spreadsheet", id="populate_spreadsheets")(populate_spreadsheets)


@node.callback(trigger=["spreadsheet"], id="fetch_sheets_delete")
async def fetch_sheets_delete(metadata: MetaDataBase, oauth_token: str, _):
    spreadsheet_id = metadata.params["spreadsheet"].value
    if spreadsheet_id:
        sheets = await list_sheets_name(oauth_token, spreadsheet_id)
        choices = [
            SelectChoice(label=sheet.label, value=sheet.value) for sheet in sheets
        ]
        metadata_dict = metadata.params["sheet"].model_dump()
        metadata_dict["component"] = Select(choices=choices)
        metadata_dict["value"] = choices[0].value
        metadata.add_param(FieldMetadata(**metadata_dict))
    return metadata


@node.on_call
async def call(inputs: Inputs, params: Params):
    sheets = await list_sheets_name(params.access_token, params.spreadsheet)
    sheet_label = None

    for sheet in sheets:
        if sheet.value == params.sheet:
            sheet_label = sheet.label
            break

    if sheet_label:
        rows = await get_values(
            spreadsheet_id=params.spreadsheet,
            sheet_name=str(sheet_label),
            access_token=params.access_token,
        )

        res = await delete_rows(
            spreadsheet_id=params.spreadsheet,
            sheet_id=params.sheet,
            access_token=params.access_token,
            start_index=0,
            end_index=len(rows),
        )
        return res
    return Response(success=False, body=f"Sheet with label {sheet_label} not found.")
