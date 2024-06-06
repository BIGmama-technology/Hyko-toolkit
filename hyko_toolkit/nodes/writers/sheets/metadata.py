from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .clear_sheet.metadata import node as clear_sheet_node
from .delete_row.metadata import node as delete_row_node
from .insert_rows.metadata import node as insert_rows_node
from .update_sheet.metadata import node as update_sheet_node

node = NodeGroup(
    name="Sheets writer",
    description="perform various spreadsheet operations.",
    icon="sheets",
    tag=Tag.utilities,
    nodes=[clear_sheet_node, delete_row_node, insert_rows_node, update_sheet_node],
)
