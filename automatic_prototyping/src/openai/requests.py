import os
from dotenv import load_dotenv

import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def chatgpt_completion(conversation: list, max_tokens: int=100, logit_bias={}) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=conversation,
        n=1,
        max_tokens=max_tokens,
        logit_bias=logit_bias,
    )
    return completion.choices[0].message.content

def gpt_completion(prompt:str, max_tokens:int=100):
    completion = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=max_tokens,
    )
    return completion.choices[0].text
    


def input_description(model_desc: str) -> str:
    prompt = f"""from a description of an AI model give a description of its inputs, model description :{model_desc} 
    input description : """
    completion = gpt_completion(prompt)
    return completion


def output_description(model_desc: str) -> str:
    prompt = f"""from a description of an AI model give a description of its outputs, model description :{model_desc} 
    output description : """
    completion = gpt_completion(prompt)
    return completion