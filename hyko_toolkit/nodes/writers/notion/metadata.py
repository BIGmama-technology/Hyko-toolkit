from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .append_to_page.metadata import node as append_to_page
from .insert_database_item.metadata import node as insert_database_item

node = NodeGroup(
    name="Notion writer",
    description="perform various notion operations.",
    icon="notion",
    tag=Tag.writers,
    nodes=[append_to_page, insert_database_item],
)
