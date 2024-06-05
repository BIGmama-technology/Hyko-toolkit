from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .clear_sheet.metadata import func as clear_sheet_node
from .delete_row.metadata import func as delete_row_node
from .insert_rows.metadata import func as insert_rows_node
from .update_sheet.metadata import func as update_sheet_node

node = ToolkitNode(
    name="Sheets writer",
    description="perform various spreadsheet operations.",
    icon="sheets",
    tag=Tag.utilities,
)


class SheetUtils(str, Enum):
    clear_sheet = "clear_sheet"
    delete_row = "delete_row"
    insert_rows = "insert_rows"
    update_sheet = "update_sheet"


@node.set_param
class Params(CoreModel):
    sheet_util: SheetUtils = field(
        description="Type of the sheet utility node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="sheet_util", id="change_sheet_util")
async def change_sheet_util_type(metadata: MetaDataBase, *_: Any):
    sheet_util = metadata.params["sheet_util"].value
    metadata.params = {}
    match sheet_util:
        case SheetUtils.clear_sheet.value:
            return clear_sheet_node.get_metadata()
        case SheetUtils.delete_row.value:
            return delete_row_node.get_metadata()
        case SheetUtils.insert_rows.value:
            return insert_rows_node.get_metadata()
        case SheetUtils.update_sheet.value:
            return update_sheet_node.get_metadata()
        case _:
            return metadata
