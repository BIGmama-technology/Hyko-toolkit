from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .recursive_character_text_splitter.metadata import (
    func as recursive_character_text_splitter_node,
)
from .remove_special_characters.metadata import func as remove_special_characters_node
from .remove_stopwords.metadata import func as remove_stopwords_node

node = ToolkitNode(
    name="NLP utilities",
    description="perform various natural language processing tasks.",
    icon="text",
    tag=Tag.utilities,
)


class TextUtils(str, Enum):
    recursive_character_text_splitter = "recursive_character_text_splitter"
    remove_special_characters = "remove_special_characters"
    remove_stopwords = "remove_stopwords"


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
        case TextUtils.recursive_character_text_splitter.value:
            return recursive_character_text_splitter_node.get_metadata()
        case TextUtils.remove_special_characters.value:
            return remove_special_characters_node.get_metadata()
        case TextUtils.remove_stopwords.value:
            return remove_stopwords_node.get_metadata()
        case _:
            return metadata
