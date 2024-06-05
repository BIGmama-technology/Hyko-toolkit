from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

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

node = ToolkitNode(
    name="Text utilities",
    description="perform various text processing tasks.",
    icon="text",
    tag=Tag.utilities,
)


class TextUtils(str, Enum):
    Concat = "concat"
    Count = "count"
    Index_mapping = "index_mapping"
    Join = "join"
    Length = "length"
    Lowercase = "lowercase"
    Padding = "padding"
    Replace = "replace"
    Reverse = "reverse"
    Slice = "slice"
    Split = "split"
    Uppercase = "uppercase"


@node.set_param
class Params(CoreModel):
    text_util: TextUtils = field(
        description="Type of the text utility node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="text_util", id="change_text_util")
async def change_text_util_type(metadata: MetaDataBase, *_: Any):
    text_util = metadata.params["text_util"].value
    metadata.params = {}
    match text_util:
        case TextUtils.Concat.value:
            return concat_node.get_metadata()
        case TextUtils.Count.value:
            return count_node.get_metadata()
        case TextUtils.Index_mapping.value:
            return index_mapping_node.get_metadata()
        case TextUtils.Join.value:
            return join_node.get_metadata()
        case TextUtils.Length.value:
            return length_node.get_metadata()
        case TextUtils.Lowercase.value:
            return lowercase_node.get_metadata()
        case TextUtils.Padding.value:
            return padding_node.get_metadata()
        case TextUtils.Replace.value:
            return replace_node.get_metadata()
        case TextUtils.Reverse.value:
            return reverse_node.get_metadata()
        case TextUtils.Slice.value:
            return slice_node.get_metadata()
        case TextUtils.Split.value:
            return split_node.get_metadata()
        case TextUtils.Uppercase.value:
            return uppercase_node.get_metadata()
        case _:
            return metadata
