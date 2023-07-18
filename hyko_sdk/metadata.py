from pydantic import BaseModel
from typing import Any, List, Optional
from .io import IOPortType, IOPort


def pmodel_to_ports(pmodel: BaseModel) -> List[IOPort]:
    
    schema = pmodel.schema()

    fields_properties: dict[str, dict[str, Any]] = schema["properties"]
    required_fields: Optional[List[str]] = schema.get("required")

    ports = []
    
    for field_name, field_props in fields_properties.items():
        field_type = field_props.get("type")

        if field_type is None:
            continue

        if field_type == "number":
            port_type = IOPortType.NUMBER
        
        elif field_type == "integer":
            port_type = IOPortType.INTEGER
        
        elif field_type == "string":
            string_format = field_props.get("format")

            if string_format is not None:
                if string_format == "image":
                    port_type = IOPortType.IMAGE
                elif string_format == "audio":
                    port_type = IOPortType.AUDIO
                elif string_format == "video":
                    port_type = IOPortType.VIDEO
                else:
                    port_type = IOPortType.STRING
            else:
                port_type = IOPortType.STRING
        
        elif field_type == "array":
            try:
                nested_type = field_props["items"]["type"]

                if nested_type == "number":
                    port_type = IOPortType.ARRAY_NUMBER
                elif nested_type == "integer":
                    port_type = IOPortType.ARRAY_INTEGER
                elif nested_type == "string":
                    try:
                        string_format = field_props["items"]["format"]
                        
                        if string_format == "image":
                            port_type = IOPortType.ARRAY_IMAGE
                        elif string_format == "audio":
                            port_type = IOPortType.ARRAY_AUDIO
                        elif string_format == "video":
                            port_type = IOPortType.VIDEO
                        else:
                            continue

                    except:
                        port_type = IOPortType.ARRAY_STRING
                else:
                    continue
        
            except:
                continue
        
        else:
            continue

        port_description = field_props.get("description")
        port_default = field_props.get("default")
        port_required = True if required_fields and field_name in required_fields else False

        ports.append(IOPort(
            name=field_name,
            type=port_type,
            description=port_description,
            required=port_required,
            default=port_default,
        ))

    return ports


class MetaData(BaseModel):
    name: str
    description: str
    version: str
    category: str
    inputs: List[IOPort]
    outputs: List[IOPort]
    params: List[IOPort]
    requires_gpu: bool