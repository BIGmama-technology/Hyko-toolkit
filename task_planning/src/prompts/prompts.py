ARGS = """["text", "image", "audio", "pdf"]"""

TASK_FORMAT = """
[{
"task_id":id, 
"task": task_name, 
"task_description": task_description, 
"dep": [dependency_task_id],
"inputs": [{"input_id":id, "input_type":type, "input_description":desc}]
"outputs": [{"output_id":generated_id, "output_type":type, "output_description":desc}] 
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

TASK_PLANNING_PROMPT = f"""Task Planning Stage: The AI assistant can parse user input to several tasks: {TASK_FORMAT}
The "dep" field denotes the ids of the previous prerequisite tasks which generate a new resource that the current task relies on. 
The input_type and output_type fields must be in {ARGS}, nothing else. The task 
must be selected from the following options: {AVAILABLE_TASKS}.
There may be multiple tasks of the same type. 
Parse out as few tasks as possible while ensuring that the user request can be resolved. 
Pay attention to the dependencies and order among tasks. 
"""
