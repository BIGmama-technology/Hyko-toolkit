from src.openai.requests import chatgpt_completion
from src.prompts.few_shot import FEW_SHOT_TASK_PLANNING
from src.prompts.prompts import TASK_PLANNING_PROMPT

import re

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