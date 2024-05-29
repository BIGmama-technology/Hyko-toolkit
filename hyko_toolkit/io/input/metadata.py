from typing import Any

from hyko_sdk.components.components import (
    Ext,
    ListComponent,
    NumberField,
    PortType,
    Select,
    SelectChoice,
    StorageSelect,
    TextField,
)
from hyko_sdk.json_schema import Item
from hyko_sdk.models import Category, CoreModel, FieldMetadata, MetaDataBase
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitNode

input_node = ToolkitNode(
    name="Input",
    task="Input",
    description="This is an input node",
    category=Category.IO,
)


@input_node.set_param
class Params(CoreModel):
    input_type: str = field(
        description="Type of the input node, when this changes it updates the output port to correspond to it.",
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


@input_node.callback(triggers=["input_type"], id="change_input_type")
async def change_input_type(metadata: MetaDataBase, *args: Any):
    input_type = metadata.params["input_type"].value
    metadata.params = {}
    match input_type:
        case "text":
            metadata.icon = "text"
            metadata.add_output(
                FieldMetadata(
                    type=PortType.STRING,
                    name="output_text",
                    description="Input text",
                    component=TextField(
                        placeholder="Input text here...", multiline=True
                    ),
                )
            )
            return metadata
        case "number":
            metadata.icon = "number"
            metadata.add_output(
                FieldMetadata(
                    type=PortType.NUMBER,
                    name="output_number",
                    description="Input number",
                    component=NumberField(placeholder="your input number"),
                )
            )
            return metadata
        case "image":
            metadata.icon = "image"
            metadata.add_output(
                FieldMetadata(
                    type=PortType.IMAGE,
                    name="output_image",
                    description="Uploaded image",
                    component=StorageSelect(supported_ext=[Ext.PNG, Ext.JPG, Ext.JPEG]),
                )
            )
            return metadata
        case "video":
            metadata.icon = "video"
            metadata.add_output(
                FieldMetadata(
                    type=PortType.VIDEO,
                    name="output_video",
                    description="Uploaded video",
                    component=StorageSelect(
                        supported_ext=[
                            Ext.MPEG,
                            Ext.WEBM,
                            Ext.MP4,
                            Ext.AVI,
                            Ext.MKV,
                            Ext.MOV,
                            Ext.WMV,
                        ]
                    ),
                )
            )
            return metadata
        case "audio":
            metadata.icon = "audio"
            metadata.add_output(
                FieldMetadata(
                    type=PortType.AUDIO,
                    name="output_audio",
                    description="Uploaded audio",
                    component=StorageSelect(
                        supported_ext=[
                            Ext.WAV,
                            Ext.MP3,
                            Ext.MPEG,
                            Ext.WEBM,
                            Ext.MP4,
                            Ext.AVI,
                            Ext.MKV,
                            Ext.MOV,
                            Ext.WMV,
                        ]
                    ),
                )
            )
            return metadata
        case "pdf":
            metadata.icon = "pdf"
            metadata.add_output(
                FieldMetadata(
                    type=PortType.PDF,
                    name="output_pdf",
                    description="Uploaded pdf",
                    component=StorageSelect(supported_ext=[Ext.PDF]),
                )
            )
            return metadata
        case "list_of_texts":
            items = Item(type=PortType.STRING)
            metadata.icon = "list"
            metadata.add_output(
                FieldMetadata(
                    type=PortType.ARRAY,
                    items=items,
                    name="output_list",
                    description="Input list of texts",
                    component=ListComponent(
                        item_component=TextField(placeholder="text item")
                    ),
                )
            )
            return metadata
        case "list_of_numbers":
            items = Item(type=PortType.NUMBER)
            metadata.icon = "list"
            metadata.add_output(
                FieldMetadata(
                    type=PortType.ARRAY,
                    items=items,
                    name="output_list",
                    description="Input list of numbers",
                    component=ListComponent(
                        item_component=TextField(placeholder="number item")
                    ),
                )
            )
            return metadata

        case _:
            return metadata
