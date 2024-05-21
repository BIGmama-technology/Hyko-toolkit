from typing import Any, Callable, Coroutine, Union

from hyko_sdk.definitions import ToolkitIO as _ToolkitIO
from hyko_sdk.definitions import ToolkitModel as _ToolkitModel
from hyko_sdk.definitions import ToolkitNode as _ToolkitNode
from hyko_sdk.models import Category, MetaDataBase

Definition = Union[
    "ToolkitNode",
    "ToolkitModel",
    "ToolkitIO",
]


class Registry:
    _registry: dict[str, Definition] = {}
    _callbacks_registry: dict[
        str, Callable[..., Coroutine[Any, Any, MetaDataBase]]
    ] = {}

    @classmethod
    def register(cls, name: str, definition: Definition):
        cls._registry[name] = definition

    @classmethod
    def get_handler(cls, name: str) -> Definition:
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
            raise ValueError(f"callback '{id}' not found")
        return cls._callbacks_registry[id]


class AllowCallback(_ToolkitNode):
    def callback(self, trigger: str, id: str):
        field = self.params.get(trigger)

        assert field, "trigger field not found in params"

        field.callback_id = id

        def warper(
            callback: Callable[..., Coroutine[Any, Any, MetaDataBase]],
        ):
            Registry.register_callback(id, callback)

        return warper


class ToolkitIO(_ToolkitIO, AllowCallback):
    def __init__(self, name: str, task: str, description: str, cost: int = 0):
        super().__init__(name=name, task=task, description=description, cost=cost)
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


class ToolkitNode(_ToolkitNode):
    def __init__(
        self, name: str, task: str, description: str, cost: int, category: Category
    ):
        super().__init__(
            name=name, task=task, description=description, cost=cost, category=category
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)


class ToolkitModel(_ToolkitModel):
    def __init__(
        self,
        name: str,
        task: str,
        description: str,
        cost: int,
        category: Category = Category.MODEL,
    ):
        super().__init__(
            name=name,
            task=task,
            description=description,
            category=category,
            cost=cost,
        )
        # Automatically register the instance upon creation
        Registry.register(self.get_metadata().image, self)
