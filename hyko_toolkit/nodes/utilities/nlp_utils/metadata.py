from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .recursive_character_text_splitter.metadata import (
    func as recursive_character_text_splitter_node,
)
from .remove_special_characters.metadata import func as remove_special_characters_node
from .remove_stopwords.metadata import func as remove_stopwords_node

node = NodeGroup(
    name="NLP utilities",
    description="perform various natural language processing tasks.",
    icon="text",
    tag=Tag.utilities,
    nodes=[
        recursive_character_text_splitter_node,
        remove_special_characters_node,
        remove_stopwords_node,
    ],
)
