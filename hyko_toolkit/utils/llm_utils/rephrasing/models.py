from typing import Any

import httpx
from hyko_sdk.models import CoreModel

from hyko_toolkit.exceptions import APICallError


class OpenaiMessage(CoreModel):
    role: str
    content: str


class OpenaiChoice(CoreModel):
    index: int
    message: OpenaiMessage
    finish_reason: str


class OpenaiUsage(CoreModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenaiResponse(CoreModel):
    created: int
    model: str
    choices: list[OpenaiChoice]
    usage: OpenaiUsage


class AnthropicContent(CoreModel):
    text: str


class AnthropicResponse(CoreModel):
    content: list[AnthropicContent]


class CohereChatHistoryItem(CoreModel):
    role: str
    message: str


class CohereResponse(CoreModel):
    text: str
    chat_history: list[CohereChatHistoryItem]


# Define a base function to handle API requests
async def fetch_response(
    url: str,
    headers: dict[str, str],
    json_payload: dict[Any, Any],
    timeout: int = 60 * 10,
):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            url, headers=headers, json=json_payload, timeout=timeout
        )
        if res.is_success:
            return res.json()
        else:
            raise APICallError(status=res.status_code, detail=res.text)


async def get_cohere_response(
    prompt: str,
    api_key: str,
    system_prompt: str,
    temperature: float,
    model: str,
) -> str:
    url = "https://api.cohere.ai/v1/chat"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"bearer {api_key}",
    }
    json = {
        "chat_history": [
            {"role": "SYSTEM", "message": system_prompt},
        ],
        "model": model,
        "message": prompt,
        "temperature": temperature,
    }

    response_data = await fetch_response(
        url=url,
        headers=headers,
        json_payload=json,
    )
    response = CohereResponse(**response_data)
    return response.chat_history[-1].message


async def get_anthropic_response(
    prompt: str,
    api_key: str,
    system_prompt: str,
    temperature: float,
    model: str,
):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    json = {
        "model": model,
        "system": system_prompt,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 2048,
    }
    response_data = await fetch_response(url=url, headers=headers, json_payload=json)
    response = AnthropicResponse(**response_data)
    return response.content[0].text


async def get_openai_response(
    prompt: str,
    api_key: str,
    system_prompt: str,
    temperature: float,
    model: str,
):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    json = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }
    response_data = await fetch_response(url=url, headers=headers, json_payload=json)

    response = OpenaiResponse(**response_data)
    return response.choices[0].message.content
