import httpx
from pydantic import Field

from hyko_sdk.models import CoreModel, Method
from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitAPI

func = ToolkitAPI(
    name="post",
    task="http_utils",
    description="Send Form Data to to a specified URL",
)


@func.set_param
class Params(CoreModel):
    url: str = Field(..., description="A list of URLs to scrape. Protocol must be either 'http' or 'https'.")
    bearer_token: str = Field(default=None, description="An optional bearer token for authentication.")


@func.set_input
class Inputs(CoreModel):
    form_input_names: list[str] = Field(
        ..., description="List of input field names."
    )
    form_input_values: list[str] = Field(
        ..., description="List of corresponding input field values."
    )


@func.set_output
class Outputs(CoreModel):
    response_success: bool = Field(default=False, description="Indicates whether the task was successful.")


def generate_form_data(input_names: list[str], input_values: list[str]) -> dict[str, str]:
    """
    Generates a dictionary of form data by pairing input field names with their corresponding values.

    Args:
        input_names (list[str]): List of input field names.
        input_values (list[str]): List of corresponding input field values.

    Returns:
        dict[str, str]: A dictionary where keys are input field names and values are input field values.
    """
    form_data = dict(zip(
        input_names,
        input_values
    ))
    return form_data


@func.on_call
async def call(inputs: Inputs, params: Params) -> Outputs:
    async with httpx.AsyncClient() as client:
        generated_form_data = generate_form_data(
            inputs.form_input_names,
            inputs.form_input_values
        )

        _headers ={
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if params.bearer_token:
            _headers["Authorization"] = f"Bearer {params.bearer_token}"


        response = await client.request(
            method=Method.post,
            url=params.url,
            headers=_headers,
            data=generated_form_data,
            timeout=60 * 10,
        )

        if not response.is_success:
            raise APICallError(status=response.status_code, detail=response.text)

        return Outputs(response_success = True)