from typing import Any, List

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
    Displayname: list[str] = field(description="List of display names of the places")
    Types: list[list[str]] = field(
        description="Nested list of types/categories for each place"
    )
    Nationalphonenumber: list[str] = field(
        description="List of national phone numbers for the places"
    )
    Internationalphonenumber: list[str] = field(
        description="List of international phone numbers for the places"
    )
    Formattedaddress: list[str] = field(
        description="List of formatted addresses for the places"
    )
    Userratingcount: list[str] = field(
        description="List of user rating counts for each place"
    )
    Current_Opening_Hours: list[str] = field(
        description="List of current opening hours information for each place"
    )
    Primary_Type: list[str] = field(
        description="List of primary types/categories for each place"
    )
    Reviews: list[str] = field(
        description="Nested list of reviews, where each review is a dictionary of various details"
    )
    Price_Level: list[str] = field(description="List of price levels for the places")
    Website_Uri: list[str] = field(description="List of website URLs for the places")
    Delivery: list[str] = field(
        description="List of boolean values indicating if delivery is available for the places"
    )
    places_data: list[str] = field(
        description="List of dictionaries containing all the above information"
    )


class DisplayName(CoreModel):
    text: str
    language_code: str = Field(alias="languageCode")


class Date(CoreModel):
    year: int
    month: int
    day: int


class TimePeriod(CoreModel):
    day: int
    hour: int
    minute: int
    date: Date


class Period(CoreModel):
    open: TimePeriod
    close: TimePeriod


class CurrentOpeningHours(CoreModel):
    open_now: bool = Field(alias="openNow")
    periods: list[Period]
    weekday_descriptions: list[str] = Field(alias="weekdayDescriptions")


class Place(CoreModel):
    display_name: DisplayName = Field(alias="displayName")
    types: List[str]
    national_phone_number: str = Field(alias="nationalPhoneNumber")
    international_phone_number: str = Field(alias="internationalPhoneNumber")
    formatted_address: str = Field(alias="formattedAddress")
    user_rating_count: int = Field(alias="userRatingCount")
    current_opening_hours: CurrentOpeningHours = Field(alias="currentOpeningHours")
    primary_type: str = Field(alias="primaryType")
    reviews: list[dict[Any, Any]]
    price_level: str = Field(alias="priceLevel", default="Not Mentioned")
    website_uri: str = Field(alias="websiteUri", default="Not Mentioned")
    delivery: bool = False


class Result(CoreModel):
    places: list[Place]


@func.on_call
async def call(inputs: Inputs, params: Params):
    payload = {"textQuery": inputs.query}
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": params.api_key,
        "maxResultCount": f"{params.max_results}",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.priceLevel,places.websiteUri,places.types,places.primaryType,places.internationalPhoneNumber,places.nationalPhoneNumber,places.userRatingCount,places.currentOpeningHours,places.delivery,places.fuelOptions,places.goodForWatchingSports,places.servesDinner,places.servesCoffee,places.servesBrunch,places.reviews,places.outdoorSeating,places.curbsidePickup,places.allowsDogs,places.menuForChildren,places.goodForChildren,places.goodForGroups",
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
        desplay_name = [
            places_response.places[i].display_name.text
            for i in range(len(places_response.places))
        ]
        reviews = [
            str(places_response.places[i].reviews)
            for i in range(len(places_response.places))
        ]
        places_data = [
            f'{{"display_name": "{desplay_name[i]}", "reviews": "{reviews[i]}"}}'
            for i in range(len(reviews))
        ]
        types = [
            places_response.places[i].types for i in range(len(places_response.places))
        ]

        formatted_address = [
            places_response.places[i].formatted_address
            for i in range(len(places_response.places))
        ]

        nationalphonenumber = [
            places_response.places[i].national_phone_number
            for i in range(len(places_response.places))
        ]
        internationalphonenumber = [
            places_response.places[i].international_phone_number
            for i in range(len(places_response.places))
        ]
        userratingcount = [
            str(places_response.places[i].user_rating_count)
            for i in range(len(places_response.places))
        ]
        currentopeninghours = [
            str(places_response.places[i].current_opening_hours)
            for i in range(len(places_response.places))
        ]
        primarytype = [
            places_response.places[i].primary_type
            for i in range(len(places_response.places))
        ]
        pricelevel = [
            places_response.places[i].price_level
            for i in range(len(places_response.places))
        ]
        websiteuri = [
            places_response.places[i].website_uri
            for i in range(len(places_response.places))
        ]
        delivery = [
            str(places_response.places[i].delivery)
            for i in range(len(places_response.places))
        ]
    else:
        raise APICallError(status=res.status_code, detail=res.text)
    return Outputs(
        Displayname=desplay_name,
        Types=types,
        Formattedaddress=formatted_address,
        Nationalphonenumber=nationalphonenumber,
        Internationalphonenumber=internationalphonenumber,
        Userratingcount=userratingcount,
        Reviews=reviews,
        Delivery=delivery,
        Website_Uri=websiteuri,
        Price_Level=pricelevel,
        Current_Opening_Hours=currentopeninghours,
        Primary_Type=primarytype,
        places_data=places_data,
    )
