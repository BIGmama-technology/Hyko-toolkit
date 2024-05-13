from hyko_sdk.components.components import Slider, TextField
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="flashrank",
    task="similarity_search",
    description="A tool employing Flashrank re-ranking capabilities for enhancing search and retrieval pipelines, leveraging state-of-the-art cross-encoders.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/similarity_search/flashrank/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/similarity_search/flashrank",
)


@func.set_input
class Inputs(CoreModel):
    docs: list[str] = field(description="Text Input.")
    query: str = field(
        description="Query or the Question to compare against the input text.",
        component=TextField(placeholder="Enter your query here"),
    )


@func.set_param
class Params(CoreModel):
    top_k: int = field(
        default=5,
        description="Number of top results to consider (default=5).",
        component=Slider(leq=1, geq=20, step=1),
    )
    score_threshold: float = field(
        default=0.5,
        description="Threshold score to filter similarity results (default=0.5).",
        component=Slider(leq=0, geq=1, step=0.01),
    )


@func.set_output
class Outputs(CoreModel):
    result: list[str] = field(description="Top K results.")
