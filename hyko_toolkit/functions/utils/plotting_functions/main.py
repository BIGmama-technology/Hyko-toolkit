from io import BytesIO
from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.io import Image
from hyko_sdk.types import Ext


def generate_violin_plot(x, y):
    sns.violinplot(x=x, y=y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Violin Plot")


def generate_area_plot(x, y):
    plt.fill_between(x, y)
    plt.xlabel("X")
    plt.ylabel("Values")
    plt.title("Area Plot")


def generate_box_plot(x, y):
    sns.boxplot(x=x, y=y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Box Plot")


def generate_line_plot(x, y):
    plt.plot(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Line Plot")


def generate_bar_plot(x, y):
    plt.bar(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Bar Plot")


def generate_scatter_plot(x, y):
    plt.scatter(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Scatter Plot")


def generate_heatmap(x, y):
    df = pd.DataFrame({"X": x, "Y": y})
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")


def generate_pair_plot(x, y):
    df = pd.DataFrame({"X": x, "Y": y})
    sns.pairplot(df)


def generate_pie_chart(y):
    counts = pd.Series(y).value_counts()
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%")
    plt.title("Pie Chart")


def generate_histogram(y):
    plt.hist(y, bins=10)
    plt.xlabel("X")
    plt.ylabel("Frequency")
    plt.title("Histogram")


def generate_plot(
    plot_type: str,
    x: Optional[List[float]] = None,
    y: Optional[List[float]] = None,
) -> Optional[BytesIO]:
    plot_functions = {
        "Violin_Plot": generate_violin_plot,
        "Area_Plot": generate_area_plot,
        "Box_Plot": generate_box_plot,
        "Line_Plot": generate_line_plot,
        "Bar_Plot": generate_bar_plot,
        "Scatter_Plot": generate_scatter_plot,
        "Heatmap": generate_heatmap,
        "Pair_Plot": generate_pair_plot,
        "Pie_Chart": generate_pie_chart,
        "Histogram": generate_histogram,
    }

    if plot_type in plot_functions:
        plot_functions[plot_type](x, y)
    else:
        return None

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return buffer


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    x = inputs.x
    y = inputs.y
    buffer = generate_plot(params.plot_type.value, x=x, y=y)
    return Outputs(image=Image(val=buffer.getvalue(), obj_ext=Ext.PNG))
