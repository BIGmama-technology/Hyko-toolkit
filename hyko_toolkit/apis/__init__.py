from hyko_sdk.definitions import ToolkitAPI

from .openai.text_completion.metadata import func as text_completion
from .openai.text_embedding.metadata import func as text_embedding

all = {
    text_completion.name: text_completion,
    text_embedding.name: text_embedding,
}


def api_handler(name: str) -> ToolkitAPI:
    return all[name]
