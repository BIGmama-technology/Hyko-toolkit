import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs
from transformers import OwlViTProcessor, OwlViTForObjectDetection
from hyko_sdk.io import image_to_base64
import torch
processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")

app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    img, err = inputs.img.decode()
    if err:
        raise HTTPException(status_code=500, detail=err.json())
    
    inputs = processor(text=[inputs.tags], images = torch.from_numpy(img), return_tensors='pt')
    # print(inputs)
    with torch.no_grad():
        outputs = model(**inputs)
    # print(img.shape)
    # target image size
    target_sizes = torch.Tensor([torch.from_numpy(img).size()[::-1]]).to(torch.int32).squeeze()[1:]
    
    print("Target Sizes: ", target_sizes)
    print("Logits", outputs.logits.shape)
    print("boxes", outputs.pred_boxes.shape)

    results = processor.post_process(outputs=outputs, target_sizes=torch.stack([target_sizes]))
    # text = inputs.tags
    boxes, scores, labels = results[0]["boxes"], results[0]["scores"], results[0]["labels"]
    # print(boxes.shape,"\n",scores.shape, "\n", labels.shape)
    
    print("Len Results", len(results))
    return Outputs(text=None)