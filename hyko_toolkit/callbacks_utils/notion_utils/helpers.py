from typing import Any


async def get_property_structure(type: str, value: str):  # noqa: C901
    if type == "title":
        return {type: [{"text": {"content": value}}]}
    elif type == "status":
        return {type: {"name": value}}
    elif type == "url":
        return {type: value}
    elif type == "phone_number":
        return {type: value}
    elif type == "number":
        return {type: int(value)}
    elif type == "checkbox":
        return {type: value}
    elif type == "date":
        return {type: {"start": value}}
    elif type == "email":
        return {type: value}
    elif type == "multi_select":
        return {type: [{"name": value}]}
    elif type == "select":
        return {type: {"name": value}}


async def get_property_value(property: dict[str, Any]):  # noqa: C901
    if property["type"] == "title":
        return property["title"][0]["text"]["content"]
    elif property["type"] == "status":
        return property["status"]["name"]
    elif property["type"] == "url":
        return property["url"]
    elif property["type"] == "phone_number":
        return property["url"]
    elif property["type"] == "number":
        return int(property["number"])
    elif property["type"] == "checkbox":
        return property["checkbox"]
    elif property["type"] == "date":
        return property["date"]["start"]
    elif property["type"] == "email":
        return property["email"]
    elif property["type"] == "multi_select":
        return property["multi_select"][0]["name"]
    elif property["type"] == "select":
        return property["select"]["name"]
