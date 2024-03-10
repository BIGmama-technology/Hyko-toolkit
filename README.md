# The HYKO SDK

- `./hyko_sdk` package which defines functions endpoitns `/on_startup`, `/on_execute`, defines hyko typing system and what downloads/uploads inputs and outputs.

- `./hyko_toolkit` A collection of functions and AI models that are available on hyko.
- `./scripts/sdk_builder.py` allows you to validate and build images of sdk functions and to push them to a registry.

Make sure to enable build kit in your docker since we are using it to mount cache for pip.


## How to add a new function

- Create a new directory inside `./sdk` with the following naming convention `./sdk/category_name/function_name/version/`
- This directory can contain anything (git repo, helper modules, requirements.txt, etc.), but most importantly it needs to contain `metadata.py` where you define the inputs, params and outputs of your function, a `main.py` where you define the `on_execute`, `on_startup` and `on_shutdown` functions and finally a `Dockerfile` for building your function.

`metadata.py`

```python
from pydantic import Field

from hyko_sdk.definitions import ToolkitFunction
from hyko_sdk.models import CoreModel

func = ToolkitFunction(
    name="name_surname",
    task="important_task",
    description="description of your function goes here",
)


@func.set_input
class Inputs(CoreModel):
    input_name: input_type = Field(..., description="Input description") # example


@func.set_param
class Params(CoreModel):
    # same as above
    pass


@func.set_output
class Outputs(CoreModel):
    # same as above
    pass
```

`main.py`

```python
from metadata import Inputs, Outputs, Params, func

@func.on_startup
async def load():
    """define here what you need to run while starting your function ex. loading model weights."""
    pass


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """define the logic of your function"""
    return Outputs()

@func
async def shutdown(x)
    """define what you need to run when shutting down your function"""
    pass

```

`Dockerfile`

```Dockerfile
FROM hyko-sdk:latest# or FROM hyko-sdk:latest in case you dont need torch and cuda

WORKDIR /app

COPY . .

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
```

- Finally run `sdk_builder.py` on your function to validate it, build its image and push it to your registry.

```bash
python ./scripts/sdk_builder.py --dir path/to/your_function --cuda --registry registry.treafik.me
```

## Resources
- [get started with docker](https://docker-curriculum.com/)
- [python exceptions](https://dev.to/derlin/diving-deeper-into-python-exceptions-cf1?ref=dailydev)
- [fastapi deprecated on_event](https://fastapi.tiangolo.com/advanced/events/)
- [Pydantic Docs](https://docs.pydantic.dev/latest/)
- [Get started with Json Schema](https://json-schema.org/learn/getting-started-step-by-step)
