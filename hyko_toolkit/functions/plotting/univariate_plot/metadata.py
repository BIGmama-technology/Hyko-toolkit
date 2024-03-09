from enum import Enum

from pydantic import Field

from hyko_sdk.definitions import SDKFunction
from hyko_sdk.io import Image
from hyko_sdk.metadata import CoreModel


class SupportedPlots(str, Enum):
    Pie_Chart = "Pie_Chart"
    Histogram = "Histogram"


func = SDKFunction(
    description="Generate various types of plots with Y input.",
)


@func.set_input
class Inputs(CoreModel):
    y: list[float] = Field(default=None, description="Y")


@func.set_param
class Params(CoreModel):
    plot_type: SupportedPlots = Field(..., description="Select Plot Type.")


@func.set_output
class Outputs(CoreModel):
    image: Image = Field(..., description="Output image.")
