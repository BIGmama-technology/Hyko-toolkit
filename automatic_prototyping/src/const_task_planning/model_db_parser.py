from pathlib import Path
import json

model_data_path = Path("../../data/")

model_metadata = []
with open(model_data_path / "huggingface_models.jsonl", "r") as db_file:
    for model in db_file:
        model = json.loads(model)
        model_metadata.append({str(model["id"]): model["description"]})

# print(model_metadata[0])
model_metadata = {k: v for model in model_metadata for k, v in model.items()}
model_metadata = {"models": model_metadata}


with open(model_data_path / "model_id_descr_map.json", "w") as file:
    json.dump(model_metadata, file)
