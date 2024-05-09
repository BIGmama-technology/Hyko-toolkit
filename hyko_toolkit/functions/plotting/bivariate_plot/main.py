from io import BytesIO
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from hyko_sdk.components.components import Ext
from hyko_sdk.io import Image
from metadata import Inputs, Outputs, Params, func


def generate_violin_plot(x: list[float], y: list[float]):
    sns.violinplot(x=x, y=y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Violin Plot")


def generate_area_plot(x: list[float], y: list[float]):
    plt.fill_between(x, y)
    plt.xlabel("X")
    plt.ylabel("Values")
    plt.title("Area Plot")


def generate_box_plot(x: list[float], y: list[float]):
    sns.boxplot(x=x, y=y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Box Plot")


def generate_line_plot(x: list[float], y: list[float]):
    plt.plot(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Line Plot")


def generate_bar_plot(x: list[float], y: list[float]):
    plt.bar(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Bar Plot")


def generate_scatter_plot(x: list[float], y: list[float]):
    plt.scatter(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Scatter Plot")


def generate_heatmap(x: list[float], y: list[float]):
    df = pd.DataFrame({"X": x, "Y": y})
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")


def generate_pair_plot(x: list[float], y: list[float]):
    df = pd.DataFrame({"X": x, "Y": y})
    sns.pairplot(df)


def generate_plot_with_two_params(
    plot_type: str,
    x: list[float],
    y: list[float],
) -> Optional[BytesIO]:
    """
    Generate various types of plots based on the specified plot_type.

    Parameters:
        plot_type (str): Type of plot to generate. Supported plot types:
            - "Violin_Plot": Generates a violin plot.
            - "Area_Plot": Generates an area plot.
            - "Box_Plot": Generates a box plot.
            - "Line_Plot": Generates a line plot.
            - "Bar_Plot": Generates a bar plot.
            - "Scatter_Plot": Generates a scatter plot.
            - "Heatmap": Generates a heatmap.
            - "Pair_Plot": Generates a pair plot.
        x : Data for the x-axis of the plot.
        y : Data for the y-axis of the plot.

    Returns:
        Optional[BytesIO]: A BytesIO object containing the generated plot image in PNG format.
            Returns None if the plot type is not supported.
    """
    if plot_type == "Violin_Plot":
        generate_violin_plot(x, y)
    elif plot_type == "Area_Plot":
        generate_area_plot(x, y)
    elif plot_type == "Box_Plot":
        generate_box_plot(x, y)
    elif plot_type == "Line_Plot":
        generate_line_plot(x, y)
    elif plot_type == "Bar_Plot":
        generate_bar_plot(x, y)
    elif plot_type == "Scatter_Plot":
        generate_scatter_plot(x, y)
    elif plot_type == "Heatmap":
        generate_heatmap(x, y)
    elif plot_type == "Pair_Plot":
        generate_pair_plot(x, y)
    else:
        return None

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return buffer


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    buffer = generate_plot_with_two_params(
        params.plot_type.value, x=inputs.x, y=inputs.y
    )
    assert buffer, "error while generating plot."

    return Outputs(
        image=await Image(obj_ext=Ext.PNG).init_from_val(val=buffer.getvalue())
    )
