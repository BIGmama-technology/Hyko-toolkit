from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="pdf_to_text",
    task="converters",
    description="Extracts text from pdf.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/converters/pdf_to_text/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/converters/pdf_to_text",
)


@func.set_input
class Inputs(CoreModel):
    pdf_file: PDF = field(description="User input pdf to be converted to text")


@func.set_output
class Outputs(CoreModel):
    text: str = field(description="Extracted text from pdf")
