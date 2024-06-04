from typing import Any, List

import httpx
from hyko_sdk.components.components import TextField
from hyko_sdk.models import Category, CoreModel, Method
from hyko_sdk.utils import field

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
    languageCode: str


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
    openNow: bool
    periods: list[Period]
    weekdayDescriptions: list[str]


class Place(CoreModel):
    displayName: DisplayName
    types: List[str]
    nationalPhoneNumber: str
    internationalPhoneNumber: str
    formattedAddress: str
    userRatingCount: int
    currentOpeningHours: CurrentOpeningHours
    primaryType: str
    reviews: list[dict[Any, Any]]
    priceLevel: str = "Not Mentioned"
    websiteUri: str = "Whithout website"
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
            places_response.places[i].displayName.text
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
            places_response.places[i].formattedAddress
            for i in range(len(places_response.places))
        ]

        nationalphonenumber = [
            places_response.places[i].nationalPhoneNumber
            for i in range(len(places_response.places))
        ]
        internationalphonenumber = [
            places_response.places[i].internationalPhoneNumber
            for i in range(len(places_response.places))
        ]
        userratingcount = [
            str(places_response.places[i].userRatingCount)
            for i in range(len(places_response.places))
        ]
        currentopeninghours = [
            str(places_response.places[i].currentOpeningHours)
            for i in range(len(places_response.places))
        ]
        primarytype = [
            places_response.places[i].primaryType
            for i in range(len(places_response.places))
        ]
        pricelevel = [
            places_response.places[i].priceLevel
            for i in range(len(places_response.places))
        ]
        websiteuri = [
            places_response.places[i].websiteUri
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
