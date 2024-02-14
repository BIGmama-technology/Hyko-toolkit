from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(description="SemanticChunker Tool.")


@func.set_input
class Inputs(CoreModel):
    text: str = Field(
        ...,
        description="Text Input",
    )


@func.set_startup_params
class StartupParams(CoreModel):
    pass


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="Processed text with semantic chunks .")
