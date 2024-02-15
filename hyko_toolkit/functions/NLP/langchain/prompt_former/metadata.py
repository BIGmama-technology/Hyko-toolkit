from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(description="SemanticChunker Tool.")


@func.set_input
class Inputs(CoreModel):
    query: str = Field(..., description="query. ")
    context: str = Field(..., description="context. ")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    result: str = Field(..., description="Prompt. ")
