from enum import Enum

import requests
from hyko_sdk.components.components import Ext, TextField
from hyko_sdk.io import PDF
from hyko_sdk.models import Category, CoreModel
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="joradp dz pdf downloader",
    task="pdf utils",
    category=Category.UTILS,
    cost=0,
    description="A function to download pdf from joradpdz.com.",
)


class Lang(str, Enum):
    arabic = "ar"
    francais = "fr"


@func.set_input
class Inputs(CoreModel):
    year: str = field(
        description="The year of the publication",
        default="2024",
        component=TextField(
            placeholder="Enter the year of the publication",
        ),
    )
    number: str = field(
        description="The number of the journal officiel",
        default="001",
    )


@func.set_param
class Params(CoreModel):
    language: Lang = field(
        description="The language of the journal",
        default=Lang.francais.value,
    )


@func.set_output
class Outputs(CoreModel):
    pdf: PDF = field(
        description="The Downloaded PDF.",
    )


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    if params.language == Lang.arabic.value:
        url = f"https://www.joradp.dz/FTP/jo-arabe/{inputs.year}/A{inputs.year}{inputs.number}.pdf"
    else:
        url = f"https://www.joradp.dz/FTP/jo-francais/{inputs.year}/F{inputs.year}{inputs.number}.pdf"
    # Send a GET request to the url
    response = requests.get(url)
    response.raise_for_status()
    # If the GET request is successful, add the content to the list
    data = response.content
    return Outputs(pdf=await PDF(obj_ext=Ext.PDF).init_from_val(val=data))
