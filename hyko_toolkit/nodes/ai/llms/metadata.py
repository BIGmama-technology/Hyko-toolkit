from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .anthropic.metadata import node as anthropic_llm_node
from .cohere.metadata import node as cohere_llm_node
from .gemini.metadata import node as gemini_llm_node
from .groq.metadata import node as groq_llm_node
from .huggingface.metadata import node as huggingface_llm_node
from .mistralai.metadata import node as mistral_ai_llm_node
from .open_router.metadata import node as open_router_llm_node
from .openai.metadata import node as openai_llm_node
from .tune_studio.metadata import node as tune_studio_llm_node

llm_node = NodeGroup(
    name="LLMs",
    description="Use text generation api from any provider : openai, cohere, gemini ...",
    tag=Tag.ai,
    icon="text",
    nodes=[
        anthropic_llm_node,
        openai_llm_node,
        gemini_llm_node,
        cohere_llm_node,
        groq_llm_node,
        huggingface_llm_node,
        tune_studio_llm_node,
        open_router_llm_node,
        mistral_ai_llm_node,
    ],
)
