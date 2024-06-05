import re
from enum import Enum
from typing import Any, Callable, Dict

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitNode

from .models import (
    get_anthropic_response,
    get_cohere_response,
    get_openai_response,
)

func = ToolkitNode(
    name="Google Kol lookup",
    task="Google",
    description="Use Google seaerch Engine for KOL lookup.",
    cost=6000,
    icon="google",
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
    topic: str = field(
        description="The Topic you want to lookup.",
        component=TextField(placeholder="Enter your query here"),
    )
    year: int = field(
        description="The year you want to lookup.",
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


@func.set_output
class Outputs(CoreModel):
    result: str = field(description="The top result.")


class GoogleResult(CoreModel):
    text: str


@func.on_call
async def call(inputs: Inputs, params: Params):
    div_pattern = re.compile(r"<div.*?>(.*?)</div>", re.DOTALL)
    url = (
        f"https://www.google.com/search?q=Top+{inputs.topic}+influencers+{inputs.year}"
    )
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.get,
            url=url,
            timeout=60 * 5,
        )
        if res.is_success:
            response = GoogleResult(text=res.text)
            text = [
                re.sub(r"<.*?>", "", match)
                for match in div_pattern.findall(response.text)
            ]
            text = " ".join(set(text))
        else:
            raise APICallError(status=res.status_code, detail=res.text)

    system_prompt = "List only the names of influencers explicitly mentioned in the provided text, in list format, and include their account names if provided in the text."
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
        prompt=text,
        api_key=params.api_key,
        model=params.model.value,
        temperature=0.2,
    )

    return Outputs(result=response)
