from enum import Enum
from typing import Any, Callable, Dict

from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

from .models import (
    get_anthropic_response,
    get_cohere_response,
    get_openai_response,
)

func = ToolkitNode(
    name="AI Text Summarizer",
    task="llm_utils",
    description="Use AI for text summarization.",
    cost=6000,
    icon="apis",
    category=Category.API,
)


class Model(str, Enum):
    gpt_4o = "gpt-4o"
    gpt_4_t = "gpt-4-turbo"
    gpt_3_5 = "gpt-3.5-turbo"
    command_r_plus = "command-r-plus"
    command_r = "command-r"
    claude3_opus = "claude-3-opus-20240229"
    claude3_sonnet = "claude-3-sonnet-20240229"
    claude3_haiku = "claude-3-haiku-20240307"


@func.set_input
class Inputs(CoreModel):
    system_prompt: str = field(
        description="System Prompt",
        default="You are a helpful and intelligent assistant.Your task is to read the text I provide and generate a concise and clear summary,capturing the main points and key details.Ensure that the summary is accurate and easy to understand.",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )
    text: str = field(
        description="text to summarize",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    model: Model = field(
        default=Model.gpt_4_t,
        description="The model to use.",
    )
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    temperature: float = field(
        default=0.2,
        description="The degree of creativity to use when generating text.",
        component=Slider(leq=1, geq=0, step=0.1),
    )


@func.set_output
class Outputs(CoreModel):
    text: str = field(description="The Summarized text.")


@func.on_call
async def call(inputs: Inputs, params: Params):
    model_to_function: Dict[Model, Callable[..., Any]] = {
        Model.gpt_4_t: get_openai_response,
        Model.gpt_4o: get_openai_response,
        Model.gpt_3_5: get_openai_response,
        Model.command_r_plus: get_cohere_response,
        Model.command_r: get_cohere_response,
        Model.claude3_opus: get_anthropic_response,
        Model.claude3_sonnet: get_anthropic_response,
        Model.claude3_haiku: get_anthropic_response,
    }

    response_function = model_to_function[params.model]

    response = await response_function(
        system_prompt=inputs.system_prompt,
        prompt=inputs.text,
        api_key=params.api_key,
        model=params.model.value,
        temperature=params.temperature,
    )

    return Outputs(text=response)
