from typing import Optional

from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="""Automatically complete and generate text based on provided input.
    This model predicts and generates the next word or sentence given a partial text input."""
)


@func.set_startup_params
class StartupParams(CoreModel):
    pass


@func.set_input
class Inputs(CoreModel):
    prompt: str = Field(..., description="User prompt to falcon-instruct")


@func.set_param
class Params(CoreModel):
    system_prompt: Optional[str] = Field(
        default=None,
        description="system-prompt or system-instruction to falcon-instruct",
    )
    max_length: int = Field(default=200, description="Max tokens to generate")
    top_k: int = Field(
        default=10, description="top_k candidates for each token generation"
    )
    temperature: float = Field(default=0.6, description="Temperature of falcon")
    top_p: float = Field(default=0.6, description="Top P of falcon")
    repetition_penalty: float = Field(
        default=10.0, description="Repetition penalty of falcon"
    )


@func.set_output
class Outputs(CoreModel):
    generated_text: str = Field(..., description="Generated Text from falcon-instruct")
