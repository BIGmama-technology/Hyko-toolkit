"""
TODO: text preprocessing and cleaning before feed model_descr to llama
"""

from llama_cpp import Llama

llm = Llama(model_path="./models/ggml-model-f16.bin")

model_descr = "A Siamese network model trained for zero-shot and few-shot text classification"

model_descr_0 = "This is model: It maps sentences & paragraphs to a 768 dimensional dense vector space."
'''
output = llm._create_completion(
    f"Given this model description: {model_descr}, describe the suitable input.\n input_description:",
    max_tokens=100,
    echo=True,
    temperature=0.6
)
print(list(output)[0]["choices"][0]["text"])
'''

output = llm._create_completion(
    f"Given this model description: {model_descr_0}, describe the suitable input.\n input_description:",
    max_tokens=50,
    echo=True,
    temperature=0.9,
    top_p=0.97
)

print(list(output)[0]["choices"][0]["text"])
