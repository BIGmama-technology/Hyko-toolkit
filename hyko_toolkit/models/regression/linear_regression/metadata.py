from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Linear regression",
    task="Regression",
    cost=0,
    description="Predicts a future value based on historical data",
    category=Category.MODEL,
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
