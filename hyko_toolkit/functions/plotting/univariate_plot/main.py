from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Image
from hyko_sdk.models import Ext


def generate_pie_chart(y: list[float]):
    counts = pd.Series(y).value_counts()
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%")
    plt.title("Pie Chart")


def generate_histogram(y: list[float]):
    plt.hist(y, bins=10)
    plt.xlabel("X")
    plt.ylabel("Frequency")
    plt.title("Histogram")


# Functions with one parameter
def generate_plot_with_one_param(plot_type: str, y: list[float]):
    """
    Generate various types of plots based on the specified plot_type.

    Parameters:
        plot_type (str): Type of plot to generate. Supported plot types:
            - "Pie_Chart": Generates a pie chart.
            - "Histogram": Generates a histogram.
        y (Optional[List[Union[float, int]]]): Data for the plot.

    Returns:
        Optional[BytesIO]: A BytesIO object containing the generated plot image in PNG format.
            Returns None if the plot type is not supported.
    """
    if plot_type == "Pie_Chart":
        generate_pie_chart(y)
    elif plot_type == "Histogram":
        generate_histogram(y)
    else:
        return None

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return buffer


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    buffer = generate_plot_with_one_param(params.plot_type.value, y=inputs.y)
    return Outputs(image=Image(val=buffer.getvalue(), obj_ext=Ext.PNG))
