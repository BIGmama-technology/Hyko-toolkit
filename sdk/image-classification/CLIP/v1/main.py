import torch
from fastapi import HTTPException
from metadata import Inputs, Outputs, Params, func
from transformers import CLIPModel, CLIPProcessor

model = None
processor = None
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


@func.on_startup
async def load():
    global model
    global processor
    if model is not None and processor is not None:
        print("Model loaded already")
        return

    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14").to(device)  # type: ignore
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")

    img = inputs.image.to_ndarray()  # type: ignore

    inputs_ = processor(
        text=params.classes,
        images=img,
        return_tensors="pt",
        padding=True,
    )

    with torch.no_grad():
        outputs = model(**inputs_.to(device))
    # image text similarity score:
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=-1)
    probs = probs.squeeze().cpu().numpy().tolist()
    max_index = 0
    for i in range(len(probs)):
        if probs[max_index] <= probs[i]:
            max_index = i

    return Outputs(output_class=params.classes[max_index])
