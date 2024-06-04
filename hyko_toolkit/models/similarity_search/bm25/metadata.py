from hyko_sdk.components.components import ListComponent, Slider, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

func = ToolkitNode(
    name="BM25",
    task="Similarity search",
    cost=0,
    description="Perform BM25 retrieval on a list of documents based on a given query.",
    category=Category.MODEL,
)


@func.set_input
class Inputs(CoreModel):
    docs: list[str] = field(
        description="Input Documents.",
        component=ListComponent(
            item_component=TextField(
                placeholder="Enter your input here", multiline=True
            ),
        ),
    )
    query: str = field(
        description="Query or the Question to compare against the input text.",
        component=TextField(placeholder="Enter your query here"),
    )


@func.set_param
class Params(CoreModel):
    top_k: int = field(
        default=3,
        description="Number of top results to consider (default=3).",
        component=Slider(leq=20, geq=1, step=1),
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = field(description="Top K results.")
