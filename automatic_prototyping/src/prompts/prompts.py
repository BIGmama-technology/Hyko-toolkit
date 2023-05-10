ARGS = """["text", "image", "audio", "pdf"]"""

TASK_FORMAT = """
[{
"task_id":unique_task_id, 
"task": task_name, 
"task_description": task_description, 
"dep": [dependency_task_id],
"inputs": [{"id":generated_unique_id, "input_type":type, "input_description":desc}]
"outputs": [{"id":generated_unique_id, "output_type":type, "output_description":desc}] 
}]
"""

AVAILABLE_TASKS = """
"token-classification", "text2text-generation", 
"summarization", "translation",  "question-answering", 
"conversational", "text-generation", "sentence-similarity", 
"tabular-classification", "object-detection", "image-classification", 
"image-to-image", "image-to-text", "text-to-image", "text-to-video", 
"image-segmentation", 
"depth-estimation", "text-to-speech", "automatic-speech-recognition", 
"audio-to-audio", "audio-classification", "canny-control", "hed-control", 
"mlsd-control", "normal-control", "openpose-control", "canny-text-to-image", 
"depth-text-to-image", "hed-text-to-image", "mlsd-text-to-image", "normal-text-to-image", 
"openpose-text-to-image", "seg-text-to-image", "convert-pdf-to-text", "visual-question-answering", 
"document-question-answering", "similarity_measure"
"""

TASK_PLANNING_PROMPT = f"""Task Planning Stage: The AI assistant can suggest the tasks needed 
to achieve from user objective, following this format: {TASK_FORMAT}
The "dep" field denotes the ids of the previous prerequisite tasks which generate needed inputs 
that the current task relies on. 
The input_type and output_type fields must be in {ARGS}, nothing else. 
example of available tasks : {AVAILABLE_TASKS}.
Use as few tasks as possible while ensuring that the user request can be resolved. 
Pay attention to the dependencies and order among tasks.
Make sure of the consistency of the input of a task and the output of it previous task using the generated unique ids.
"""
