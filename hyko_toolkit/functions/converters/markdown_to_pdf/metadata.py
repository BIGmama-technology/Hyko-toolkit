from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel
from pydantic import Field

from hyko_toolkit.registry import ToolkitFunction

func = ToolkitFunction(
    name="markdown_to_pdf",
    task="converters",
    description="Convert Markdown content to PDF format.",
    absolute_dockerfile_path="./toolkit/hyko_toolkit/functions/converters/markdown_to_pdf/Dockerfile",
    docker_context="./toolkit/hyko_toolkit/functions/converters/markdown_to_pdf",
)


@func.set_input
class Inputs(CoreModel):
    markdown_string: str = Field(..., description="The Markdown content to convert.")


@func.set_output
class Outputs(CoreModel):
    pdf: PDF = Field(..., description="PDF File .")
