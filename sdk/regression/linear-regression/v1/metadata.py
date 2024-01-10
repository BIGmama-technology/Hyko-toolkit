from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Predicts a future value based on historical data",
)


@func.set_input
class Inputs(CoreModel):
    predict_x: float = Field(
        ..., description="X axis value for which to predict Y axis value"
    )


@func.set_param
class Params(CoreModel):
    historical_x: list[float] = Field(..., description="Historical data of X axis")
    historical_y: list[float] = Field(..., description="Historical data of Y axis")


@func.set_output
class Outputs(CoreModel):
    predict_y: float = Field(..., description="Predicted Y axis value")
