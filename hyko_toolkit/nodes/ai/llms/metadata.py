from hyko_sdk.models import Tag

from hyko_toolkit.node_group import NodeGroup

from .anthropic.metadata import func as anthropic_llm
from .cohere.metadata import func as cohere_llm
from .gemini.metadata import func as gemini_llm
from .groq.metadata import func as groq_llm
from .huggingface.metadata import func as huggingface_llm
from .mistralai.metadata import func as mistral_ai_llm
from .open_router.metadata import func as open_router_llm
from .openai.metadata import func as openai_llm
from .tune_studio.metadata import func as tune_studio_llm

llm_node = NodeGroup(
    name="LLMs",
    description="Use text generation api from any provider : openai, cohere, gemini ...",
    tag=Tag.ai,
    icon="text",
    nodes=[
        anthropic_llm,
        openai_llm,
        gemini_llm,
        cohere_llm,
        groq_llm,
        huggingface_llm,
        tune_studio_llm,
        open_router_llm,
        mistral_ai_llm,
    ],
)
