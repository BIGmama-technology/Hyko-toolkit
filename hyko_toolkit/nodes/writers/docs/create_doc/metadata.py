import json

from hyko_sdk.components.components import (
    TextField,
)
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import (
    CoreModel,
    SupportedProviders,
)
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.docs_utils import create_document, write_to_document
from hyko_toolkit.callbacks_utils.sheets_utils import Response

node = ToolkitNode(
    name="Create Docs file",
    description="create a Google Docs file and write content to it.",
    icon="docs",
    cost=200,
    auth=SupportedProviders.DOCS,
)


@node.set_input
class Inputs(CoreModel):
    title: str = field(
        description="Title of the document to be created",
        component=TextField(placeholder="Enter document title here"),
    )
    body: str = field(
        description="Body content to be written to the document",
        component=TextField(placeholder="Enter document body here"),
    )


@node.set_param
class Params(CoreModel):
    access_token: str = field(
        description="OAuth access token for Google Docs API", hidden=True
    )


@node.on_call
async def call(inputs: Inputs, params: Params):
    document = await create_document(inputs.title, params.access_token)

    response = await write_to_document(
        document["documentId"],  # type: ignore
        inputs.body,
        params.access_token,
    )

    return Response(success=True, body=json.dumps(response))
