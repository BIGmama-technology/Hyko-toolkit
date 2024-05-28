from typing import Any, Callable, Coroutine, Optional

from hyko_sdk.definitions import ToolkitNode as _ToolkitNode
from hyko_sdk.models import Category, Icon, MetaDataBase


class Registry:
    _registry: dict[str, "ToolkitNode"] = {}
    _callbacks_registry: dict[
        str, Callable[..., Coroutine[Any, Any, MetaDataBase]]
    ] = {}

    @classmethod
    def register(cls, name: str, definition: "ToolkitNode"):
        cls._registry[name] = definition

    @classmethod
    def get_handler(cls, name: str) -> "ToolkitNode":
        if name not in cls._registry:
            raise ValueError(f"handler '{name}' not found")
        return cls._registry[name]

    @classmethod
    def get_all_metadata(cls):
        return [definition.get_metadata() for definition in cls._registry.values()]

    @classmethod
    def register_callback(
        cls, id: str, callback: Callable[..., Coroutine[Any, Any, MetaDataBase]]
    ):
        cls._callbacks_registry[id] = callback

    @classmethod
    def get_callback(cls, id: str):
        if id not in cls._callbacks_registry:
            raise ValueError(f"callback {id} not found")
        return cls._callbacks_registry[id]


class ToolkitNode(_ToolkitNode):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        category: Category,
        icon: Optional[Icon] = "io",
        cost: int = 0,
        auth: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            task=task,
            description=description,
            cost=cost,
            icon=icon,
            category=category,
            auth=auth,
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)

    def callback(self, triggers: list[str], id: str):
        for trigger in triggers:
            field = self.params.get(trigger)
            assert field, "trigger field not found in params"
            field.callback_id = id

        def wrapper(
            callback: Callable[..., Coroutine[Any, Any, MetaDataBase]],
        ):
            Registry.register_callback(id, callback)

        return wrapper
