import os

from dotenv import load_dotenv

import openai
from src.prompts.few_shot import FEW_SHOT_TASK_PLANNING
from src.prompts.prompts import TASK_PLANNING_PROMPT

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def chatgpt_completion(conversation: str) -> str:
    conversation = [{"role": "user", "content": conversation}]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
    )
    return completion.choices[0].message.content


def task_planning(prompt: str):
    conversation = [{"role": "system", "content": TASK_PLANNING_PROMPT}]
    conversation += FEW_SHOT_TASK_PLANNING
    conversation += [{"role": "user", "content": prompt}]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
    )
    # task_planning_result = eval(completion.choices[0].message.content)
    # return task_planning_result
    return completion.choices[0].message.content


def model_classification(task: str, meta: str) -> str:
    conversation = [
        {"role": "system", "content": MODEL_CLASSIFICATION_PROMPT(meta, task)}
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
    )
    choice_id = eval(completion.choices[0].message.content)["id"]
    return choice_id
