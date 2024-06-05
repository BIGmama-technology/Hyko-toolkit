from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .concat.metadata import func as concat_node
from .count.metadata import func as count_node
from .index_mapping.metadata import func as index_mapping_node
from .join.metadata import func as join_node
from .length.metadata import func as length_node
from .lowercase.metadata import func as lowercase_node
from .padding.metadata import func as padding_node
from .replace.metadata import func as replace_node
from .reverse.metadata import func as reverse_node
from .slice.metadata import func as slice_node
from .split.metadata import func as split_node
from .uppercase.metadata import func as uppercase_node

node = NodeGroup(
    name="Text utilities",
    description="perform various text processing tasks.",
    icon="text",
    tag=Tag.utilities,
    nodes=[
        concat_node,
        count_node,
        index_mapping_node,
        join_node,
        length_node,
        lowercase_node,
        padding_node,
        replace_node,
        reverse_node,
        slice_node,
        split_node,
        uppercase_node,
    ],
)
