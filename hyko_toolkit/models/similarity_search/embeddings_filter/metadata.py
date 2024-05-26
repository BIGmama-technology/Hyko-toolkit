from hyko_sdk.components.components import ListComponent, Slider, TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="Embeddings filter",
    task="Similarity search",
    cost=0,
    description="Document compressor that uses embeddings to drop documents unrelated to the query.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/similarity_search/embeddings_filter/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/similarity_search/embeddings_filter",
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
    embeddings_similarity_threshold: float = field(
        default=0.6,
        description="Threshold for determining when two documents are similar enough to be considered redundant (default=0.6).",
        component=Slider(leq=1, geq=0, step=0.01),
    )
    top_k: int = field(
        default=5,
        description="Number of top results to consider (default=5).",
        component=Slider(leq=20, geq=1, step=1),
    )
    score_threshold: float = field(
        default=0.5,
        description="Threshold score to filter similarity results (default=0.5).",
        component=Slider(leq=1, geq=0, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = field(description="Top K results.")
