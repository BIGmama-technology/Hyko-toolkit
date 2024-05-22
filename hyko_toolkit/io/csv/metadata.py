import io

import pandas as pd
from hyko_sdk.components.components import Ext, PortType, StorageSelect
from hyko_sdk.io import CSV
from hyko_sdk.json_schema import Item
from hyko_sdk.models import CoreModel, FieldMetadata, MetaData, StorageConfig
from hyko_sdk.utils import field

from hyko_toolkit.registry import ToolkitIO

input_node = ToolkitIO(
    name="CSV",
    task="inputs",
    description="Upload csv.",
)


@input_node.set_param
class Param(CoreModel):
    csv: CSV = field(
        description="Uploaded csv",
        component=StorageSelect(supported_ext=[Ext.CSV]),
    )


@input_node.callback(triggers=["csv"], id="add_csv_outputs")
async def add_csv_outputs(
    metadata: MetaData, access_token: str, refresh_token: str
) -> MetaData:
    StorageConfig.configure(
        access_token=access_token,
        refresh_token=refresh_token,
        host="http://backend:8000",
    )
    dtype_map = {
        "bool": PortType.BOOLEAN,
        "int64": PortType.INTEGER,
        "float64": PortType.NUMBER,
        "object": PortType.STRING,
    }

    csv = await CSV(obj_ext=Ext.CSV, file_name=metadata.params["csv"].value).get_data()

    df = pd.read_csv(io.BytesIO(csv))  # type: ignore
    columns = df.dtypes.to_dict()  # type: ignore
    metadata.outputs = {}
    for column_name, column_type in columns.items():  # type: ignore
        metadata.add_output(
            FieldMetadata(
                type=PortType.ARRAY,
                name=column_name,
                description=f"Column {column_name} with type {dtype_map.get(str(column_type), PortType.ANY)}",  # type: ignore
                items=Item(type=dtype_map.get(str(column_type), PortType.ANY)),  # type: ignore
            )
        )

    return metadata
