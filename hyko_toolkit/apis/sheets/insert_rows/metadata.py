from hyko_sdk.components.components import (
    ListComponent,
    PortType,
    Select,
    SelectChoice,
    TextField,
)
from hyko_sdk.json_schema import Item
from hyko_sdk.models import (
    Category,
    CoreModel,
    FieldMetadata,
    MetaDataBase,
    SupportedProviders,
)
from hyko_sdk.utils import field
from pydantic import BaseModel, ConfigDict

from hyko_toolkit.callbacks_utils.sheets_utils import (
    Dimension,
    get_sheet_columns,
    insert_google_sheet_values,
    list_sheets_name,
    populate_sheets,
    populate_spreadsheets,
)
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Insert rows to sheets",
    task="Insert rows to sheets",
    description="Add one or more new rows in a specific spreadsheet.",
    category=Category.API,
    cost=600,
    auth=SupportedProviders.SHEETS,
    icon="sheets",
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
    access_token: str = field(description="oauth access token", hidden=True)


func.callback(triggers=["spreadsheet"], id="populate_spreadsheets", is_refresh=True)(
    populate_spreadsheets
)


func.callback(triggers=["sheet"], id="populate_sheets_insert", is_refresh=True)(
    populate_sheets
)


@func.callback(triggers=["sheet"], id="add_sheet_insert_rows_inputs")
async def add_sheet_insert_rows_values(
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
                        type=PortType.ARRAY,
                        name=column,
                        description=column,
                        items=Item(type=PortType.STRING),
                        component=ListComponent(
                            item_component=TextField(placeholder="Enter a value")
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


@func.callback(triggers=["spreadsheet"], id="fetch_sheets_insert")
async def fetch_sheets_insert(metadata: MetaDataBase, oauth_token: str, _):
    spreadsheet_id = metadata.params["spreadsheet"].value
    if spreadsheet_id:
        sheets = await list_sheets_name(oauth_token, spreadsheet_id)
        choices = [
            SelectChoice(label=sheet.label, value=sheet.label) for sheet in sheets
        ]
        metadata_dict = metadata.params["sheet"].model_dump()
        metadata_dict["component"] = Select(choices=choices)
        metadata_dict["value"] = choices[0].value
        metadata.add_param(FieldMetadata(**metadata_dict))

        metadata = await add_sheet_insert_rows_values(metadata, oauth_token, _)

    return metadata


@func.on_call
async def call(inputs: Inputs, params: Params):
    inputs_json = inputs.model_dump()
    values = [inputs_json[key] for key in inputs_json]
    res = await insert_google_sheet_values(
        access_token=params.access_token,
        spreadsheet_id=params.spreadsheet,
        sheet_name=params.sheet,
        values=values,
        dimension=Dimension.COLUMNS,
    )
    return res
