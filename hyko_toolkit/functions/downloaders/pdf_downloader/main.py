import requests
from hyko_sdk.components.components import Ext
from hyko_sdk.io import PDF
from hyko_sdk.models import CoreModel

from .metadata import Inputs, Outputs, func


@func.on_call
async def main(inputs: Inputs, params: CoreModel) -> Outputs:
    # Send a GET request to the url
    response = requests.get(inputs.url)
    response.raise_for_status()
    # If the GET request is successful, add the content to the list
    data = response.content
    return Outputs(pdf=await PDF(obj_ext=Ext.PDF).init_from_val(val=data))
