import openai
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if params.system_prompt is None:
        messages = [
            {"role": "user", "content": inputs.prompt},
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": params.system_prompt,
            },
            {"role": "user", "content": inputs.prompt},
        ]

    chat_completion = await openai.ChatCompletion.acreate(
        model=params.model,
        messages=messages,
        api_key=params.api_key,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    completion: str = chat_completion.choices[0].message.content  # type: ignore

    return Outputs(completion_text=completion)
