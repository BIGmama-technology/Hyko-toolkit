from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .arithmetic.metadata import func as arithmetic_node
from .random.metadata import func as random_node
from .range.metadata import func as range_node
from .round.metadata import func as round_node

node = ToolkitNode(
    name="Math utilities",
    description="perform various mathematical operations.",
    icon="number",
    tag=Tag.utilities,
)


class MathUtils(str, Enum):
    Arithmetic = "arithmetic"
    Random = "random"
    Range = "range"
    Round = "round"


@node.set_param
class Params(CoreModel):
    math_util: MathUtils = field(
        description="Type of the math utility node, when this changes it updates the output port to correspond to it.",
    )


@node.callback(trigger="math_util", id="change_math_util")
async def change_math_util_type(metadata: MetaDataBase, *_: Any):
    math_util = metadata.params["math_util"].value
    metadata.params = {}
    match math_util:
        case MathUtils.Arithmetic.value:
            return arithmetic_node.get_metadata()
        case MathUtils.Random.value:
            return random_node.get_metadata()
        case MathUtils.Range.value:
            return range_node.get_metadata()
        case MathUtils.Round.value:
            return round_node.get_metadata()
        case _:
            return metadata
