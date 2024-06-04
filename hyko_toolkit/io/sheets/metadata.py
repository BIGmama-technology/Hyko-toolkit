from hyko_sdk.components.components import (
    PortType,
    RefreshableSelect,
    SelectChoice,
)
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.json_schema import Item
from hyko_sdk.models import (
    Category,
    CoreModel,
    FieldMetadata,
    MetaDataBase,
    SupportedProviders,
)
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.sheets_utils import (
    get_sheet_columns,
    list_sheets_name,
    populate_sheets,
    populate_spreadsheets,
)

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
        description="Spreadsheet file to append to.",
        component=RefreshableSelect(choices=[], callback_id="populate_spreadsheets"),
    )
    sheet: str = field(
        description="Sheet",
        component=RefreshableSelect(choices=[], callback_id="populate_sheets"),
        hidden=True,
    )


input_node.callback(trigger="spreadsheet", id="populate_spreadsheets")(
    populate_spreadsheets
)


input_node.callback(trigger="sheet", id="populate_sheets")(populate_sheets)


@input_node.callback(trigger="sheet", id="update_sheets_names")
async def update_sheets_names(
    metadata: MetaDataBase, oauth_token: str, _
) -> MetaDataBase:
    spreadsheet_id = metadata.params["spreadsheet"].value
    sheet_name = metadata.params["sheet"].value
    if spreadsheet_id and sheet_name:
        columns = await get_sheet_columns(oauth_token, spreadsheet_id, sheet_name)
        metadata.outputs = {}
        for column in columns:
            metadata.add_output(
                FieldMetadata(
                    type=PortType.ARRAY,
                    name=column,
                    items=Item(type=PortType.STRING),
                    description=f"Column {column}",
                )
            )

    return metadata


@input_node.callback(trigger="spreadsheet", id="update_sheets_outputs")
async def update_sheets_node(
    metadata: MetaDataBase, oauth_token: str, _
) -> MetaDataBase:
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
        metadata.add_param(FieldMetadata(**metadata_dict))

        metadata = await update_sheets_names(metadata, oauth_token, _)

    return metadata
