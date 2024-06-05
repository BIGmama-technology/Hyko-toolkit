from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import CoreModel, MetaDataBase, Tag
from hyko_sdk.utils import field

from .anthropic.metadata import func as anthropic_llm
from .cohere.metadata import func as cohere_llm
from .gemini.metadata import func as gemini_llm
from .groq.metadata import func as groq_llm
from .huggingface.metadata import func as huggingface_llm
from .mistralai.metadata import func as mistral_ai_llm
from .open_router.metadata import func as open_router_llm
from .openai.metadata import func as openai_llm
from .tune_studio.metadata import func as tune_studio_llm

llm_node = ToolkitNode(
    name="Text Generation APIs",
    description="Use text generation api from any provider : openai, cohere, gemini ...",
    tag=Tag.ai,
    cost=0,
)


class Providers(str, Enum):
    anthropic = "Anthropic"
    openai = "Openai"
    gemini = "Gemini"
    cohere = "Cohere"
    groq = "Groq"
    huggingface = "Huggingface"
    tune_studio = "Tune-studio"
    open_router = "Open-router"
    mistral_ai = "Mistral ai"


@llm_node.set_param
class Params(CoreModel):
    provider: Providers = field(
        description="Type of the input node, when this changes it updates the output port to correspond to it.",
    )


@llm_node.callback(trigger=["provider"], id="change_llm_provider")
async def change_input_type(metadata: MetaDataBase, *args: Any) -> MetaDataBase:
    provider = metadata.params["provider"].value
    assert isinstance(provider, str)
    match provider:
        case Providers.anthropic.value:
            return anthropic_llm.get_metadata()
        case Providers.openai.value:
            return openai_llm.get_metadata()
        case Providers.gemini.value:
            return gemini_llm.get_metadata()
        case Providers.cohere.value:
            return cohere_llm.get_metadata()
        case Providers.groq.value:
            return groq_llm.get_metadata()
        case Providers.huggingface.value:
            return huggingface_llm.get_metadata()
        case Providers.tune_studio.value:
            return tune_studio_llm.get_metadata()
        case Providers.open_router.value:
            return open_router_llm.get_metadata()
        case Providers.mistral_ai.value:
            return mistral_ai_llm.get_metadata()
        case _:
            return metadata
