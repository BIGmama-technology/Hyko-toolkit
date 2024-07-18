from hyko_sdk.components.components import RefreshableSelect, TextField
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import (
    CoreModel,
    SupportedProviders,
)
from hyko_sdk.utils import field

from hyko_toolkit.utils.docs_utils import (
    populate_documents,
    write_to_document,
)
from hyko_toolkit.utils.sheets_utils import Response

node = ToolkitNode(
    name="Append text to Google Docs file",
    description="Appends the provided text to the specified Google Docs document.",
    icon="docs",
    cost=200,
    auth=SupportedProviders.DOCS,
)


@node.set_input
class Inputs(CoreModel):
    text: str = field(
        description="Text to append to the Google Docs document",
        component=TextField(placeholder="Enter text here"),
    )


@node.set_param
class Params(CoreModel):
    access_token: str = field(
        description="OAuth access token for Google Docs API", hidden=True
    )
    document: str = field(
        description="Document to append text to.",
        component=RefreshableSelect(choices=[], callback_id="populate_documents"),
    )


node.callback(trigger="document", id="populate_documents")(populate_documents)


@node.on_call
async def call(inputs: Inputs, params: Params):
    response = await write_to_document(
        params.document, inputs.text, params.access_token
    )
    return Response(success=True, body=response.model_dump_json())
