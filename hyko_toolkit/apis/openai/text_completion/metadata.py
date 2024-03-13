from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import ToolkitAPI
from hyko_sdk.models import CoreModel, Method

func = ToolkitAPI(
    name="text_completion",
    task="openai",
    description="Use openai api for text completion.",
)


class OpenaiModel(str, Enum):
    gpt_4 = "gpt-4"
    chatgpt = "gpt-3.5-turbo"


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = Field(
        default="You are a helpful assistant", description="generated text."
    )
    prompt: str = Field(..., description="Input prompt.")


@func.set_param
class Params(CoreModel):
    api_key: str = Field(default="", description="API key")
    openai_model: OpenaiModel = Field(
        default=OpenaiModel.chatgpt,
        description="Openai model to use.",
    )
    max_tokens: int = Field(
        default=1024,
        description="The maximum number of tokens that can be generated in the chat completion.",
    )
    temperature: int = Field(
        default=1,
        description="What sampling temperature to use, between 0 and 2, defaults to 1.",
    )


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="generated text.")


func.on_call(
    method=Method.post,
    url="https://api.openai.com/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Params.api_key}",
    },
    body={
        "model": Params.openai_model,
        "max_tokens": Params.max_tokens,
        "temperature": Params.temperature,
        "messages": [
            {"role": "system", "content": Inputs.system_prompt},
            {"role": "user", "content": Inputs.prompt},
        ],
    },
    response={
        "choices": [
            {
                "message": {
                    "content": Outputs.result,
                },
            }
        ],
    },
)
