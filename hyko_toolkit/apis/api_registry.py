from hyko_sdk.definitions import ToolkitAPI as _ToolkitAPI


class APIRegistry:
    _registry: dict[str, _ToolkitAPI] = {}

    @classmethod
    def register(cls, name: str, api: _ToolkitAPI):
        cls._registry[name] = api

    @classmethod
    def get_handler(cls, name: str) -> _ToolkitAPI:
        if name not in cls._registry:
            raise ValueError(f"API handler '{name}' not found")
        return cls._registry[name]


class ToolkitAPI(_ToolkitAPI):
    def __init__(self, name: str, task: str, description: str):
        # Automatically register the instance upon creation
        super().__init__(name=name, task=task, description=description)
        APIRegistry.register(
            self.get_base_metadata().image,
            self,
        )
