import os
import tempfile

import pandas as pd
import PyPDF2
from hyko_sdk.components.components import Ext, StorageSelect
from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.io import Document
from hyko_sdk.models import (
    CoreModel,
)
from hyko_sdk.utils import field

from hyko_toolkit.nodes.core.document.utils import get_docx_text

input_node = ToolkitNode(
    name="Document input",
    description="Upload doc, docx, pdf, xls ....",
    icon="pdf",
    is_input=True,
)


@input_node.set_param
class Param(CoreModel):
    document: Document = field(
        description="Uploaded Document",
        component=StorageSelect(supported_ext=[Ext.CSV, Ext.XLSX, Ext.PDF, Ext.DOCX]),
    )


@input_node.set_output
class Outputs(CoreModel):
    document_text: str = field(description="document text")


@input_node.on_call
async def execute(input: CoreModel, params: Param):
    table_data = await params.document.get_data()

    with tempfile.NamedTemporaryFile(
        delete=True,
    ) as temp:
        temp.write(table_data)
        temp.flush()
        _, obj_ext = os.path.splitext(params.document.get_name())
        obj_ext = Ext(obj_ext.lstrip("."))

        match obj_ext:
            case Ext.XLSX:
                document = pd.read_excel(temp.name).to_markdown()  # type: ignore
            case Ext.PDF:
                pdf_reader = PyPDF2.PdfReader(temp)
                document = ""
                for page in pdf_reader.pages:
                    document += page.extract_text()
            case Ext.DOCX:
                document: str = get_docx_text(temp.name)
            case Ext.CSV:
                document: str = pd.read_csv(temp.name).to_csv()  # type: ignore
            case _:
                raise Exception("file type not supported")

    return Outputs(document_text=document)
