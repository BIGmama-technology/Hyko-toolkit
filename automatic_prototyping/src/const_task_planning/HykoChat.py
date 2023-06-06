import json
from typing import List, Dict, Optional

input_ = f"""
        <TASK-LIST>
            <TASK>Perform an exploratory data analysis on the provided dataset to understand the data and identify any potential issues or patterns.</TASK>
            <TASK>Preprocess the data, including cleaning, normalization, and feature engineering, to prepare it for training the AI model.</TASK>
            <TASK>Develop a supervised machine learning model using the preprocessed data to predict crashes with an accuracy of above 80%.</TASK>
            <TASK>Test and validate the performance of the AI model on a separate dataset to ensure its generalizability and reliability.</TASK>
            <TASK>Integrate the AI model into the vehicle's processing unit and develop a system to alert the driver and send a notification to the cloud about the predicted crash.</TASK>
            <TASK>Develop a prototype of the AI-enhanced safety solution and test it in real-world scenarios to evaluate its effectiveness and identify any potential improvements or modifications.</TASK>
            <TASK>Ensure that the AI-enhanced safety solution meets any necessary regulations and requirements for use in the automotive industry.</TASK>
        </TASK-LIST>
        """


def Parse_Tasks(tasks_: str) -> List[str]:
    tasks_ = tasks_.replace("<TASK-LIST>", "")
    tasks_ = tasks_.replace("</TASK-LIST>", "")
    tasks_ = tasks_.split("</TASK>")
    tasks_ = [item_.replace("<TASK>", "").strip() for item_ in tasks_]
    return tasks_


output_ = Parse_Tasks(input_)
for i_ in output_:
    print(i_)
    print()
