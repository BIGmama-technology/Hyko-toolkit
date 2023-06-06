r"""
This file contains the Dict (JSON) structure of the prompt used with Llama
to obtain technical task plans from a raw ScopeBook OBJ
"""

from llama_cpp import Llama

# from scoping import ScopeBook
from typing import Dict, List

TASK_PLAN_CONTROL_TOKENS = {
    "INPUT_PROBLEM": "<RAW_PROBLEM>",
    "INPUT_ANSWER": "<RAW_ANSWER>",
    "OUTPUT_PROBLEM": "<TECHNICAL_PROBLEM>",
    "OUTPUT_ANSWER": "<TECHNICAL_ANSWER>",
    "BEGIN_TOKEN": "<START>",
    "END_TOKEN": "<END>",
}

'''
class Task_Prompt:
    r"""
    Prompt class
    """
    operational_prompts: List[str] = list()

    def __init__(
        self,
        scopebook : ScopeBook = None,
        ctrl_toks: Dict = TASK_PLAN_CONTROL_TOKENS,
    ):
        self.context = scopebook.scopebook_context
        self.ctrl_toks = ctrl_toks
        self.operational_pbs = scopebook.scopebook_operational_pbs
        self.create_prompts(self.context, self.operational_pbs)

    def plug_context(self, context: str = None):
        r"""
        Premade context structure, plugged with actual context from user
        """

        TASK_PLAN_CONTEXT = f"""Context: You are an AI professional with access to pretrained machine learning models.
                                Instruction: Propose an AI-based solution to "RAW PROBLEM" using Software and AI. 
                                Provide technical steps of the solution in the form of bullet points in technical terms.
                             """
        return TASK_PLAN_CONTEXT

    def create_prompts(self, context : str = None, operational_pbs: List[str] = None):

        task_plan_context = self.plug_context(context=context)
        for operational_ in operational_pbs[1:][0]:

            self.operational_prompts.append(
                f"""RAW_PROBLEM: {operational_}.
                {task_plan_context}
                AI solution:
                """
            )

    def __repr__(self) -> "Task_Prompt":
        return self.operational_prompts
'''

class Task_Prompt:
    
    r"""
    Prompt class
    """
    operational_pbs: List[str] = list()
    operational_prompts: List[str] = list()
    CONTEXT: str = f"""Context: You are an AI professional with access to pretrained machine learning models.
                        Instruction: Expand on the given solutions with AI models and architectures to use.
                        Provide technical steps of the solution in the form of bullet points.
                        """
    def __init__(
        self,
        chat_tasks: str = None,
    ):
        self.chat_tasks = chat_tasks
        self.create_prompts(self.operational_pbs)

    def Parse_Tasks(self, tasks_: str) -> List[str]:
        tasks_ = tasks_.replace("<TASK-LIST>", "")
        tasks_ = tasks_.replace("</TASK-LIST>", "")
        tasks_ = tasks_.replace(".", "")
        tasks_ = tasks_.split("</TASK>")
        tasks_ = [item_.replace("<TASK>", "").strip() for item_ in tasks_]
        return tasks_

    def create_prompts(self, input_chat_str: str = None):
        operational_pbs = self.Parse_Tasks(self.chat_tasks)
        for operational_ in operational_pbs:
            self.operational_prompts.append(
                f"""RAW_PROBLEM: {operational_}.
                {self.CONTEXT}
                AI solution:
                """
            )