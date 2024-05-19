from enum import Enum

from hyko_sdk.components.components import Search, Slider, TextField
from hyko_sdk.models import CoreModel, ModelMetaData
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils import huggingface_models_search
from hyko_toolkit.registry import ToolkitModel

func = ToolkitModel(
    name="translation",
    task="natural_language_processing",
    cost=0,
    description="Hugging Face translation task",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/models/natural_language_processing/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/models/natural_language_processing/translation",
)


class SupportedLanguages(str, Enum):
    english = "en"
    arabic = "ar"
    french = "fr"
    spanish = "es"
    chinese = "zh"
    german = "de"
    russian = "ru"


@func.set_startup_params
class StartupParams(CoreModel):
    hugging_face_model: str = field(
        description="Model",
        component=Search(placeholder="Search translation model"),
    )
    device_map: str = field(description="Device map (Auto, CPU or GPU)")


@func.set_input
class Inputs(CoreModel):
    original_text: str = field(
        description="The text to translate.",
        component=TextField(placeholder="Enter your text here", multiline=True),
    )


@func.set_param
class Params(CoreModel):
    max_new_tokens: int = field(
        default=30, description="Cap newly generated content length"
    )
    top_k: int = field(
        default=2,
        description="Number of top predictions to return (default: 2).",
        component=Slider(leq=5, geq=0, step=1),
    )
    temperature: float = field(
        default=0.5,
        description="Randomness (fluency vs. creativity)",
        component=Slider(leq=1, geq=0, step=1),
    )
    top_p: float = field(
        default=0.5,
        description="Focus high-probability words (diversity control)",
        component=Slider(leq=1, geq=0, step=0.1),
    )
    src_lang: SupportedLanguages = field(
        default=None, description="The source Language."
    )
    tgt_lang: SupportedLanguages = field(
        default=None, description="The target Language."
    )


@func.set_output
class Outputs(CoreModel):
    translation_text: str = field(description="The translated text.")


@func.callback(triggers=["hugging_face_model"], id="translation_search")
async def add_search_results(
    metadata: ModelMetaData, access_token: str, refresh_token: str
) -> ModelMetaData:
    return await huggingface_models_search(metadata)
