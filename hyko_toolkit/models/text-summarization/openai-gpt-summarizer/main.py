import openai
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    chat_completion = await openai.ChatCompletion.acreate(
        model=params.model,
        messages=[
            {
                "role": "system",
                "content": "Summarize this",
            },
            {
                "role": "user",
                "content": inputs.text,
            },
        ],
        api_key=params.api_key,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
    )

    completion: str = chat_completion.choices[0].message.content  # type: ignore

    return Outputs(summary=completion)
