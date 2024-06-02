from hyko_sdk.components.components import PortType, Select, SelectChoice
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
    sheet: str = field(
        description="Sheet name",
        component=Select(choices=[]),
    )


input_node.callback(
    triggers=["spreadsheet"], id="populate_spreadsheets", is_refresh=True
)(populate_spreadsheets)


input_node.callback(triggers=["sheet"], id="populate_sheets", is_refresh=True)(
    populate_sheets
)


@input_node.callback(triggers=["sheet"], id="update_sheets_names")
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


@input_node.callback(triggers=["spreadsheet"], id="update_sheets_outputs")
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
        metadata_dict["component"] = Select(choices=choices)
        metadata.params["sheet"].value = {}
        metadata.add_param(FieldMetadata(**metadata_dict))
        columns = await get_sheet_columns(oauth_token, spreadsheet_id, "")
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
