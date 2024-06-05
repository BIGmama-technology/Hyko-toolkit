from enum import Enum
from typing import Any, Callable, Dict

from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

from .models import (
    get_anthropic_response,
    get_cohere_response,
    get_openai_response,
)

func = ToolkitNode(
    name="AI Text Rephraser",
    task="llm_utils",
    description="Use AI for text rephrasing.",
    cost=6000,
    icon="apis",
    category=Category.API,
)


class Lang(str, Enum):
    ara = "arabic"
    en = "english"
    fr = "french"


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
    text: str = field(
        description="text to Rephrase",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    source_lang: Lang = field(
        default=Lang.fr,
        description="The source language of the text.",
    )
    target_lang: Lang = field(
        default=Lang.ara,
        description="The target language of the text.",
    )
    model: Model = field(
        default=Model.gpt_4_t,
        description="The model to use.",
    )
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )


@func.set_output
class Outputs(CoreModel):
    text: str = field(description="The Summarized text.")


@func.on_call
async def call(inputs: Inputs, params: Params):
    system_prompt = f"""Please translate the following text between {params.source_lang.value} and {params.target_lang.value},
    ensuring the meaning and context of the original text are accurately conveyed in the translated version.
    If the input is in {params.source_lang.value},
    please translate it to {params.target_lang.value}.
    If the input is in {params.target_lang.value},
    please translate it to {params.source_lang.value} ,
    Please do not include any additional text or explanation in your response, only the translated text."""
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
        system_prompt=system_prompt,
        prompt=f"Text to Rephrase : \n{inputs.text}",
        api_key=params.api_key,
        model=params.model.value,
        temperature=0.4,
    )

    return Outputs(text=response)
