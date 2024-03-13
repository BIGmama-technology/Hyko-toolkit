from openai.text_completion.metadata import func as text_completion

from hyko_sdk.definitions import ToolkitAPI

all = {text_completion.name: text_completion}


def api_handler(name: str) -> ToolkitAPI:
    return all[name]
