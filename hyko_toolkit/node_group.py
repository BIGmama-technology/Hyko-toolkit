from enum import Enum
from typing import Any

from hyko_sdk.definitions import ToolkitNode
from hyko_sdk.models import Icon, MetaDataBase, Tag
from hyko_sdk.utils import field
from pydantic.main import create_model  # type: ignore


class NodeGroup(ToolkitNode):
    def __init__(
        self,
        name: str,
        description: str,
        icon: Icon | None,
        tag: Tag,
        nodes: list[ToolkitNode],
    ):
        super().__init__(name, description, icon=icon, tag=tag)
        self.nodes = nodes

        choices = Enum("Choices", [(node.name, node.name) for node in self.nodes])
        params = create_model(
            "Params",
            choice=(choices, field(description="choose your node wisely")),
        )
        self.set_param(params)
        self.callback(trigger="choice", id=name)(self.choose_node)

    async def choose_node(self, metadata: MetaDataBase, *_: Any):
        trigger = metadata.params.get("choice")
        assert trigger, "trigger not found in params"

        case_map = {node.name: node for node in self.nodes}
        value = trigger.value
        assert value, "choice value is not set"
        chosen_node = case_map.get(value)
        if chosen_node:
            return chosen_node.get_metadata()

        return metadata
