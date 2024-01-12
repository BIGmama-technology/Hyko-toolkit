# The HYKO SDK

- `./hyko-sdk` package which defines functions endpoitns `/on_startup`, `/on_execute`, defines hyko typing system and what downloads/uploads inputs and outputs.

- `./sdk` A collection of functions and AI models that are available on hyko.
- `./scripts/sdk_builder.py` allows you to validate and build images of sdk functions and to push them to a registry.

## To publish

Before publishing a new version of `hyko-sdk` make sure to update its version in `pyproject.toml`

Follow this convetion by [npm](https://docs.npmjs.com/about-semantic-versioning)

| Code status                            | Stage           | Rule                                                | Example version |
|----------------------------------------|-----------------|-----------------------------------------------------|-----------------|
| First release                          | New product     | Start with 1.0.0                                    | 1.0.0           |
| Backward compatible bug fixes          | Patch release   | Increment the third digit                          | 1.0.1           |
| Backward compatible new features       | Minor release   | Increment the middle digit and reset last digit to zero | 1.1.0           |
| Changes that break backward compatibility | Major release | Increment the first digit and reset middle and last digits to zero | 2.0.0 |

Generate a `pypi` token and add it to configure poetry to use it

```bash
poetry config pypi-token.pypi your-pypi-token
```

Now you can build and publish

```bash
poetry build
poetry publish
```

## How to add a new function

- create a new directory inside `./sdk` with the following naming convention `./sdk/category_name/function_name/version/`
- this directory can contain anything (git repo, helper modules, requirements.txt, etc.), but most importantly it needs to contain `metadata.py` where you define the inputs, params and outputs of your function, a `main.py` where you define the `on_execute`, `on_startup` and `on_shutdown` functions and finally a `Dockerfile` for building your function.

`metadata.py`

```python
from pydantic import Field

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
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
    pass

```

`Dockerfile`

```Dockerfile
FROM torch-cuda:latest # or FROM hyko-sdk:latest in case you dont need torch and cuda

WORKDIR /app

COPY . .

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
```

- finally run `sdk_builder.py` on your function to validate it, build its image and push it to your registry.

```bash
python ./scripts/sdk_builder.py --dir path/to/your_function --cuda --registry registry.treafik.me
```

## Resources

- [fastapi deprecated on_event](https://fastapi.tiangolo.com/advanced/events/)
