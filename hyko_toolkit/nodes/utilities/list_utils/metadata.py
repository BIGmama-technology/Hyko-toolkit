from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .any.metadata import func as any_node
from .append.metadata import func as append_node
from .count.metadata import func as count_node
from .extend.metadata import func as extend_node
from .index.metadata import func as index_node
from .insert.metadata import func as insert_node
from .len.metadata import func as len_node
from .max.metadata import func as max_node
from .min.metadata import func as min_node
from .pop.metadata import func as pop_node
from .remove.metadata import func as remove_node
from .reverse.metadata import func as reverse_node
from .slice.metadata import func as slice_node
from .sort.metadata import func as sort_node
from .sum.metadata import func as sum_node

node = ToolkitNode(
    name="List utilities",
    description="perform various list operations.",
    icon="list",
    tag=Tag.utilities,
)


class ListUtils(str, Enum):
    Any = "any"
    Append = "append"
    Count = "count"
    Extend = "extend"
    Index = "index"
    Insert = "insert"
    Len = "len"
    Max = "max"
    Min = "min"
    Pop = "pop"
    Remove = "remove"
    Reverse = "reverse"
    Slice = "slice"
    Sort = "sort"
    Sum = "sum"


@node.set_param
class Params(CoreModel):
    list_util: ListUtils = field(
        description="Type of the list utility node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="list_util", id="change_list_util")
async def change_list_util_type(metadata: MetaDataBase, *_: Any):
    list_util = metadata.params["list_util"].value
    metadata.params = {}
    match list_util:
        case ListUtils.Any.value:
            return any_node.get_metadata()
        case ListUtils.Append.value:
            return append_node.get_metadata()
        case ListUtils.Count.value:
            return count_node.get_metadata()
        case ListUtils.Extend.value:
            return extend_node.get_metadata()
        case ListUtils.Index.value:
            return index_node.get_metadata()
        case ListUtils.Insert.value:
            return insert_node.get_metadata()
        case ListUtils.Len.value:
            return len_node.get_metadata()
        case ListUtils.Max.value:
            return max_node.get_metadata()
        case ListUtils.Min.value:
            return min_node.get_metadata()
        case ListUtils.Pop.value:
            return pop_node.get_metadata()
        case ListUtils.Remove.value:
            return remove_node.get_metadata()
        case ListUtils.Reverse.value:
            return reverse_node.get_metadata()
        case ListUtils.Slice.value:
            return slice_node.get_metadata()
        case ListUtils.Sort.value:
            return sort_node.get_metadata()
        case ListUtils.Sum.value:
            return sum_node.get_metadata()
        case _:
            return metadata
