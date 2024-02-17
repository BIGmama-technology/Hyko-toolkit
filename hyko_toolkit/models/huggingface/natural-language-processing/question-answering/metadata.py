from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Hugging Face Question Answering task",
)


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = Field(..., description="Model")
    device_map: str = Field(..., description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    question: str = Field(..., description="Input question")
    context: str = Field(..., description="Context from which to answer the question")


@func.set_param
class Params(CoreModel):
    pass


@func.set_output
class Outputs(CoreModel):
    answer: str = Field(..., description="Answer to the question")
    start: int = Field(..., description="Start index")
    end: int = Field(..., description="End index")
    score: float = Field(..., description="Score of the answer")
