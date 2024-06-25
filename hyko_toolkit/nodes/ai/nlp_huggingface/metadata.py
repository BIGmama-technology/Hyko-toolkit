from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .fill_mask.metadata import node as fill_mask_node
from .question_answering.metadata import node as question_answering_node
from .summarization.metadata import node as summarization_node
from .text_classification.metadata import node as text_classification_node
from .text_generation.metadata import node as text_generation_node
from .translation.metadata import node as translation_node
from .zero_shot_classification.metadata import node as zero_shot_classification_node

node = NodeGroup(
    name="NLP Huggingface APIs",
    description="Huggingface NLP models.",
    icon="hf",
    tag=Tag.ai,
    nodes=[
        fill_mask_node,
        question_answering_node,
        summarization_node,
        text_classification_node,
        text_generation_node,
        translation_node,
        zero_shot_classification_node,
    ],
)
