from hyko_sdk.components.components import RefreshableSelect
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import (
    CoreModel,
    SupportedProviders,
)
from hyko_sdk.utils import field

from hyko_toolkit.callbacks_utils.docs_utils import (
    populate_documents,
    read_from_document,
)

node = ToolkitNode(
    name="Docs reader",
    description="Upload and read content from a Google Docs file.",
    icon="docs",
    auth=SupportedProviders.DOCS,
)


@node.set_output
class Outputs(CoreModel):
    text: str = field(description="Document content.")


@node.set_param
class Params(CoreModel):
    access_token: str = field(
        description="OAuth access token for Google Docs API", hidden=True
    )
    document: str = field(
        description="Document to read",
        component=RefreshableSelect(choices=[], callback_id="populate_documents"),
    )


node.callback(trigger="document", id="populate_documents")(populate_documents)


@node.on_call
async def call(params: Params) -> Outputs:
    document_text = await read_from_document(params.document, params.access_token)

    return Outputs(text=document_text)
