import json


def save_json(filename, json_data):
    with open(filename, "w") as f:
        json.dump(json_data, f)
