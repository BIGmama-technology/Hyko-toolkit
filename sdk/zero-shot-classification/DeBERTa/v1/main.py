from typing import List

import torch
from fastapi.exceptions import HTTPException
from pydantic import Field
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Perform zero-shot classification on text input, assigning it to one of the predefined classes",
    requires_gpu=False,
)


class Inputs(CoreModel):
    text: str = Field(..., description="Input text to be classified")


class Params(CoreModel):
    classes: List[str] = Field(..., description="A list of possible classes")


class Outputs(CoreModel):
    output_class: str = Field(..., description="The predicted class")


model = None
tokenizer = None
device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")


@func.on_startup
async def load():
    global model
    global tokenizer
    if model is not None and tokenizer is not None:
        print("Model loaded already")
        return

    model_name = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    premise = inputs.text

    input = tokenizer(premise, premise, truncation=True, return_tensors="pt")

    input_ids = input["input_ids"].to(device)

    with torch.no_grad():
        output = model(input_ids)

    probs = torch.softmax(output["logits"][0], -1).tolist()
    max_index = 0
    for i in range(len(probs)):
        if probs[max_index] <= probs[i]:
            max_index = i

    return Outputs(output_class=params.classes[max_index])
