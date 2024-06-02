from hyko_sdk.components.components import Search, Slider, TextField
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.huggingface_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Question answering",
    task="Natural language processing",
    cost=0,
    icon="hf",
    description="Hugging Face Question Answering task",
    category=Category.MODEL,
)


@func.set_input
class Inputs(CoreModel):
    question: str = field(
        description="Input question",
        component=TextField(placeholder="Enter your question here", multiline=True),
    )
    context: str = field(
        description="Context from which to answer the question",
        component=TextField(placeholder="Enter your context here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search question answering model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")
    top_k: int = field(
        default=1,
        description="Keep best k options (default:1).",
        component=Slider(leq=5, geq=1, step=1),
    )
    doc_stride: int = field(
        default=128,
        description="The stride of the splitting sliding window (default:128).",
    )


@func.set_output
class Outputs(CoreModel):
    answer: str = field(description="Answer to the question")
    start: int = field(description="Start index")
    end: int = field(description="End index")
    score: float = field(description="Score of the answer")


func.callback(triggers=["hugging_face_model"], id="hugging_face_search")(
    huggingface_models_search
)
