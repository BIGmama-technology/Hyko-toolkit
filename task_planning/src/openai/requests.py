import os
import re

from dotenv import load_dotenv

import openai
from src.prompts.few_shot import FEW_SHOT_TASK_PLANNING
from src.prompts.prompts import TASK_PLANNING_PROMPT

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


def input_description(prompt: str) -> str:
    """
    max_tokens: 200
    n : 1
    """
    conversation = [
        {
            "role": "system",
            "content": "from a description of an AI model give a description of the inputs",
        },
        {"role": "user", "content": prompt},
    ]
    completion = chatgpt_completion(conversation)
    return completion


def output_description(prompt: str) -> str:
    """
    max_tokens: 200
    n : 1
    """
    conversation = [
        {
            "role": "system",
            "content": "from a description of an AI model give a description of the outputs",
        },
        {"role": "user", "content": prompt},
    ]
    completion = chatgpt_completion(conversation)
    return completion


def few_shot_task_planning(prompt: str):
    conversation = [{"role": "system", "content": TASK_PLANNING_PROMPT}]
    conversation += FEW_SHOT_TASK_PLANNING
    conversation += [{"role": "user", "content": prompt}]
    completion = chatgpt_completion(conversation)

    # task_planning_result = eval(completion.choices[0].message.content)
    # return task_planning_result
    return completion

def zero_shot_task_planning(subject: str, logit_bias={58:100}):
    conversation = [{"role": "system", "content": TASK_PLANNING_PROMPT}]
    conversation += [{"role": "user", "content": "give a task plan (a json between two ```) for this subject : " + subject}]
    completion = chatgpt_completion(conversation, max_tokens=1000)

    result = re.search(r'```json(.+?)```', completion, flags=re.DOTALL)
    if result:
        extracted_text = result.group(1)
        return extracted_text
    
    result = re.search(r'```(.+?)```', completion, flags=re.DOTALL)
    if result:
        extracted_text = result.group(1)
        return extracted_text
    
    raise Exception("error parsing output of zero_shot_task_planning")