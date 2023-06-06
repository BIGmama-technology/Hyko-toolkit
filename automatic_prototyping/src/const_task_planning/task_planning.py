r"""
Task planning from ScopeBook
"""

from llama_cpp import Llama
from scoping import ScopeBook
from pathlib import Path
import logging
from typing import List
from prompts.prompt import *
import numpy as np

logging.basicConfig(level=logging.DEBUG)


def get_llama_from_cache(n_ctx: int = 1024):
    r"""
    load Llama from cached dir
    """
    LLM_MODEL_BIN_PATH = Path("/home/lotfi/llama/models/13B")
    BIN_FILE = "ggml-model-f16.bin"
    llama_instance = Llama(
        model_path=str(LLM_MODEL_BIN_PATH / BIN_FILE),
        verbose=False,
        n_ctx=n_ctx,
        n_gpu_layers=16,
    )

    logging.debug(f" Loaded Model from file: {BIN_FILE}\n")
    return llama_instance

class TaskPlan:
    r"""
    TaskPlan Class
    """

    task_plan_: List[str] = []

    """
    def __init__(self, scopebook: ScopeBook = None):
        # self.raw_context_ = scopebook.scopebook_context
        # self.raw_problems = scopebook.scopebook_operational_pbs
        self.raw_scopebook = scopebook
    """

    def __init__(self, chat_str: str) -> None:
        self.chat_str = chat_str

    def generate_task_plan(self, LLM: Llama) -> "TaskPlan":
        r"""
        raw_to_TP: converts  a raw ScopeBook Body into a strcutured Task Plan (populate self.task_plan)
            args: ScopeBook.scopebook_body: Dict of problem keys, list[answers] values
            return : None
        """

        # Create prompt from scopebook
        # prompts_ = Task_Prompt(scopebook=self.raw_scopebook).operational_prompts
        prompts_ = Task_Prompt(self.chat_str)

        # Genrerate relative tasks for each operational_prompt
        for prompt in prompts_.operational_prompts:
            output = LLM._create_completion(
                prompt=prompt,
                max_tokens=len(LLM.tokenize(prompt.encode("utf-8"))),
                temperature=0.87,  # 0.7
                top_p=0.8,  # 0.7
                top_k=5,  # 2
                repeat_penalty=5,
            )

            task_ = list(output)[0]["choices"][0]["text"]
            # task_ = list(output)[0]['choices'][0]['text']
            print("PROMPT: ", prompt)
            print()
            print("adding Task: |", task_, "| to Task_Plan")
            print()
            print()
            self.task_plan_.append(task_)

if __name__ == "__main__":
    input_chat_1 = f"""
                    <TASK-LIST>
                        <TASK>Digitize the client's 1,000 paper records containing sales data, including dates, items sold, individual prices, and total prices.</TASK>
                        <TASK>Develop an AI model to analyze the digitized sales data and identify the most popular menu items and their respective prices.</TASK>
                        <TASK>Use the AI model's insights to make data-driven decisions for the new location, focusing on menu items, pricing, and potential improvements.</TASK>
                    </TASK-LIST>
                    """

    input_chat_2 = f"""
                    <TASK-LIST>
                        TASK>Perform an exploratory data analysis on the provided dataset to understand the data and identify any potential issues or patterns.</TASK>
                        <TASK>Preprocess the data, including cleaning, normalization, and feature engineering, to prepare it for training the AI model.</TASK>
                        <TASK>Develop a supervised machine learning model using the preprocessed data to predict crashes with an accuracy of above 80%.</TASK>
                        <TASK>Test and validate the performance of the AI model on a separate dataset to ensure its generalizability and reliability.</TASK>
                        <TASK>Integrate the AI model into the vehicle's processing unit and develop a system to alert the driver and send a notification to the cloud about the predicted crash.</TASK>
                        <TASK>Develop a prototype of the AI-enhanced safety solution and test it in real-world scenarios to evaluate its effectiveness and identify any potential improvements or modifications.</TASK>
                        <TASK>Ensure that the AI-enhanced safety solution meets any necessary regulations and requirements for use in the automotive industry.</TASK>
                    </TASK-LIST>
                    """

    input_chat_3 = f"""
                    <TASK-LIST>
                        <TASK>Generate design options based on specific parameters and constraints.</TASK>
                        <TASK>Generate multiple design alternatives using provided goals and criteria</TASK>
                        <TASK>Assistance in identifying patterns, trends, and inspiration sources</TASK>
                        <TASK>Automate repetitive tasks such as sorting and categorizing design assets.</TASK>
                        <TASK>Provide real-time suggestions and recommendations by analyzing the design elements, styles, and patterns in existing designs or a designer's work and offer suggestions for improvements, alternative layouts, or complementary color schemes.</TASK>
                        <TASK>Analyze user data, identify patterns and trends in user behavior to optimize user experience, layout, and information architecture.</TASK>
                        <TASK>Enhance 3D modeling and simulation by automating parts of the process. </TASK>
                        <TASK>Generate 3D models from 2D sketches or descriptions </TASK>
                        <TASK>Optimize designs for specific criteria (e.g., weight reduction, structural integrity) </TASK>
                        <TASK>Automate repetitive design tasks (e.g. resizing images, creating design variations, or generating design assets (e.g., logos, icons) based on specific design criteria.) </TASK>
                        <TASK>Provide feedback on designs </TASK>
                        <TASK>Allow designer to give directions for recommandation </TASK>
                    </TASK-LIST>
                    """
    
    input_chat_4 = f"""
                    <TASK-LIST>
                        <TASK> Develop an AI solution to predict crashes using Lidar, proximity, and camera sensor data. </TASK>
                        <TASK> Create a prototype of the AI solution for the client's safety system. </TASK>
                        <TASK> Refine and integrate the AI solution into the client's safety system based on further requirements and constraints. </TASK>
                    </TASK-LIST>                        
                    """
    
    input_chat_5 = f"""
                    <TASK LIST>
                        <TASK>Procedural Content Generation: Generate game content such as levels, maps, terrain, puzzles procedurally. </TASK>
                        <TASK>Natural Language Processing: Enable voice-activated controls, chatbot, dialogue systems withing the game. </TASK>
                        <TASK>Game Balancing: Adjust game parameters according to player behavior to maintain an optimal difficulty level.</TASK>
                        <TASK>Player behavior analysis: Personalize gameplay experiences according to player preferences.
                        Improve player retention and satisfaction.</TASK>
                        <TASK>Visuals and animation: Enhance graphics, animation and visual effects.
                        Generate realistic texture synthesis.</TASK>
                        <TASK>Playtesting and Quality Assurance: Simulate player behavior, identify bugs, provide performance insights.</TASK>
                        <TASK>Game Design Assistance: Give suggestions to generate ideas and optimize mechanics, prototype new game concepts.
                        Analyze player feedback, iterate on game design elements more efficiently.</TASK>
                    </TASK LIST>
                    """
    
    llama_instance = get_llama_from_cache(n_ctx=1024)
    task_plan = TaskPlan(chat_str=input_chat_1)
    task_plan.generate_task_plan(LLM=llama_instance)

    print(task_plan.task_plan_)
