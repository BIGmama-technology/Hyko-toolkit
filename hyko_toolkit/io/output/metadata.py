from typing import Any

from hyko_sdk.components.components import (
    AudioPreview,
    ImagePreview,
    ListComponent,
    NumberField,
    PDFPreview,
    PortType,
    Select,
    SelectChoice,
    TextField,
    TextPreview,
    VideoPreview,
)
from hyko_sdk.json_schema import Item
from hyko_sdk.models import Category, CoreModel, FieldMetadata, MetaDataBase
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

output_node = ToolkitNode(
    name="Output",
    task="Outputs",
    description="This is an output node",
    category=Category.IO,
)


@output_node.set_param
class Params(CoreModel):
    output_type: str = field(
        description="Type of the output node, when this changes it updates the input port to correspond to it.",
        component=Select(
            choices=[
                SelectChoice(label="Text", value="text"),
                SelectChoice(label="Number", value="number"),
                SelectChoice(label="Image", value="image"),
                SelectChoice(label="Video", value="video"),
                SelectChoice(label="Audio", value="audio"),
                SelectChoice(label="Pdf", value="pdf"),
                SelectChoice(label="List of Texts", value="list_of_texts"),
                SelectChoice(label="List of numbers", value="list_of_numbers"),
            ]
        ),
    )


@output_node.callback(trigger="output_type", id="change_output_type")
async def change_output_type(metadata: MetaDataBase, *_: Any):
    output_type = metadata.params["output_type"].value
    metadata.params = {}
    match output_type:
        case "text":
            metadata.icon = "text"
            metadata.add_input(
                FieldMetadata(
                    type=PortType.STRING,
                    name="output_text",
                    description="Output text",
                    component=TextPreview(),
                )
            )
            return metadata
        case "number":
            metadata.icon = "number"
            metadata.add_input(
                FieldMetadata(
                    type=PortType.NUMBER,
                    name="output_number",
                    description="Output number",
                    component=NumberField(
                        placeholder="your output number", freezed=True
                    ),
                )
            )
            return metadata
        case "image":
            metadata.icon = "image"
            metadata.add_input(
                FieldMetadata(
                    type=PortType.IMAGE,
                    name="output_image",
                    description="Uploaded image",
                    component=ImagePreview(),
                )
            )
            return metadata
        case "video":
            metadata.icon = "video"
            metadata.add_input(
                FieldMetadata(
                    type=PortType.VIDEO,
                    name="output_video",
                    description="Uploaded video",
                    component=VideoPreview(),
                )
            )
            return metadata
        case "audio":
            metadata.icon = "audio"
            metadata.add_input(
                FieldMetadata(
                    type=PortType.AUDIO,
                    name="output_audio",
                    description="Uploaded audio",
                    component=AudioPreview(),
                )
            )
            return metadata
        case "pdf":
            metadata.icon = "pdf"
            metadata.add_input(
                FieldMetadata(
                    type=PortType.PDF,
                    name="output_pdf",
                    description="Uploaded pdf",
                    component=PDFPreview(),
                )
            )
            return metadata
        case "list_of_texts":
            items = Item(type=PortType.STRING)
            metadata.icon = "list"
            metadata.add_input(
                FieldMetadata(
                    type=PortType.ARRAY,
                    items=items,
                    name="output_list",
                    description="Output list of texts",
                    component=ListComponent(
                        freezed=True, item_component=TextField(placeholder="text item")
                    ),
                )
            )
            return metadata
        case "list_of_numbers":
            items = Item(type=PortType.NUMBER)
            metadata.icon = "list"
            metadata.add_input(
                FieldMetadata(
                    type=PortType.ARRAY,
                    items=items,
                    name="output_list",
                    description="Output list of numbers",
                    component=ListComponent(
                        freezed=True,
                        item_component=TextField(placeholder="number item"),
                    ),
                )
            )
            return metadata

        case _:
            return metadata
