from typing import Any, Optional

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field
from pydantic import Field

from hyko_toolkit.exceptions import APICallError
from hyko_toolkit.registry import ToolkitNode

func = ToolkitNode(
    name="Google Places",
    task="Google",
    category=Category.API,
    description="Use  Google Places API for Search.",
    cost=100,
    icon="google",
)


@func.set_input
class Inputs(CoreModel):
    query: str = field(
        description="The search query.",
        component=TextField(placeholder="Enter your query here"),
    )


@func.set_param
class Params(CoreModel):
    api_key: str = field(
        description="API key", component=TextField(placeholder="API KEY", secret=True)
    )
    max_results: int = field(
        default=5,
        description="Maximum number of results.",
    )


@func.set_output
class Outputs(CoreModel):
    display_name: list[str] = field(
        description="List of display names of the places", alias="Displayname"
    )
    Formatted_address: list[str] = field(
        description="List of formatted addresses of the places",
    )
    website_uris: list[str] = field(description="List of website uris of the places")
    reviews: list[str] = field(description="List of reviews of the places")


class DisplayName(CoreModel):
    text: str
    language_code: str = Field(alias="languageCode")


class Place(CoreModel):
    display_name: DisplayName = Field(alias="displayName")
    formatted_address: str = Field(alias="formattedAddress")
    website_uri: str = Field(alias="websiteUri", default="Not Mentioned")
    reviews: Optional[list[Any]] = []


class Result(CoreModel):
    places: list[Place]


@func.on_call
async def call(inputs: Inputs, params: Params):
    payload = {"textQuery": inputs.query}
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": params.api_key,
        "maxResultCount": f"{params.max_results}",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.websiteUri,places.reviews",
    }
    async with httpx.AsyncClient() as client:
        res = await client.request(
            method=Method.post,
            url="https://places.googleapis.com/v1/places:searchText",
            headers=headers,
            json=payload,
            timeout=600 * 100,
        )
    if res.is_success:
        places_response = Result(**res.json())
        display_name = [place.display_name.text for place in places_response.places]
        formatted_address = [
            place.formatted_address for place in places_response.places
        ]
        website_uris = [place.website_uri for place in places_response.places]
        reviews = [str(place.reviews) for place in places_response.places]
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(
        display_name=display_name,
        Formatted_address=formatted_address,
        website_uris=website_uris,
        reviews=reviews,
    )
