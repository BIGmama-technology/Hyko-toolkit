from hyko_sdk.components.components import ListComponent, Slider, TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="E5 faiss",
    task="Similarity search",
    cost=0,
    description="Tool for computing similarity scores based on a given threshold.",
)


@func.set_input
class Inputs(CoreModel):
    docs: list[str] = field(
        description="Text Input.",
        component=ListComponent(
            item_component=TextField(
                placeholder="Your document should be here.", multiline=True
            )
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
        component=Slider(leq=30, geq=1, step=1),
    )
    score_threshold: float = field(
        default=0.4,
        description="Threshold score to filter similarity results (default=0.4).",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = field(description="Top K results. ")
