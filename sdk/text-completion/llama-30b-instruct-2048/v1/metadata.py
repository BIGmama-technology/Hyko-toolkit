from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Meta Llama-2 30B instruct text generation model.",
)


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="User prompt")


@func.set_param
class Params(CoreModel):
    system_prompt: str = Field(
        default=None, description="system-prompt or system-instruction"
    )
    max_new_tokens: int = Field(default=256, description="Max tokens to generate")


@func.set_output
class Outputs(CoreModel):
    generated_text: str = Field(..., description="Generated Text from falcon-instruct")
