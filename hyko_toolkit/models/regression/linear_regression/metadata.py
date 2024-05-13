from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="linear_regression",
    task="regression",
    description="Predicts a future value based on historical data",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/regression/linear_regression/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/regression/linear_regression",
)


@func.set_input
class Inputs(CoreModel):
    predict_x: float = field(
        description="X axis value for which to predict Y axis value"
    )
    historical_x: list[float] = field(description="Historical data of X axis")
    historical_y: list[float] = field(description="Historical data of Y axis")


@func.set_output
class Outputs(CoreModel):
    predict_y: float = field(description="Predicted Y axis value")
