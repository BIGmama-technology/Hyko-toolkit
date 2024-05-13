from hyko_sdk.components.components import ListComponent, Slider, TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="hybrid_search",
    task="similarity_search",
    description="Executes simultaneous BM25 keyword matching and document similarity searches on input documents.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/similarity_search/hybrid_search/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/similarity_search/hybrid_search",
)


@func.set_input
class Inputs(CoreModel):
    docs: list[str] = field(
        description="Input Documents.",
        component=ListComponent(
            item_component=TextField(
                placeholder="Enter your input here", multiline=True
            )
        ),
    )
    query: str = field(
        description="Query or the Question to compare against the input text.",
        component=TextField(placeholder="Enter your query here"),
    )


@func.set_param
class Params(CoreModel):
    bm25_k: int = field(
        default=3,
        description="Number of top results to consider in Best Matching Algorithm (BM25) (default=3).",
        component=Slider(leq=1, geq=20, step=1),
    )
    faiss_k: int = field(
        default=3,
        description="Number of top results to consider in Similarity Search Algorithm (default=3).",
        component=Slider(leq=1, geq=20, step=1),
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = field(description="Top K results.")
