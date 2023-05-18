r"""
This file implements field-completion using 7B-Llama, loads model_db as json generates input and output describtions for each model
and stores everything in a JSON file as model_metadata Database

TODO: Implement Model_db_class using custom generation_config_ for input_description and output_description

get_func:
    

"""

from llama_cpp import Llama
from pathlib import Path
from transformers import pipeline
from typing import Any, Optional, List, Dict
import json

MODEL_JSON_FILE_PATH = Path("../../data")
LLM_MODEL_BIN_PATH = Path("./models")

class generation_config_:
    def __init__(
        self,
        suffix: Optional[str] = None,
        max_tokens: int = 16,
        temperature: float = 0.8,
        top_p: float = 0.95,
        logprobs: Optional[int] = None,
        echo: bool = False,
        stop: Optional[List[str]] = [],
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        repeat_penalty: float = 1.1,
        top_k: int = 40,
        stream: bool = False,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_tau: float = 5.0,
        mirostat_eta: float = 0.1,
    ):
        self.suffix = suffix
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.logprobs = logprobs
        self.echo = echo
        self.stop = stop
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.repeat_penalty = repeat_penalty
        self.top_k = top_k
        self.stream = stream
        self.tfs_z = tfs_z
        self.mirostat_mode = mirostat_mode
        self.mirostat_tau = mirostat_tau
        self.mirostat_eta = mirostat_eta

    def get_attribute_dict(self):
        generation_args = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        ]

        attr_dict = dict()
        for attr_name in generation_args:
            attr_value = getattr(self, attr_name)
            attr_dict.update({attr_name :  attr_value})
        
        del generation_args
        return attr_dict

class Model_DB:
    model_db_dict = None

    def __init__(
        self,
        json_file : str = MODEL_JSON_FILE_PATH / "model_id_descr_map.json",
        llm_file : str = LLM_MODEL_BIN_PATH / "ggml-model-f16.bin",
        summerizer_model: str = None,
        sum_min : int  = 5,
        sum_max : int = 10

    ):
        self.model_bin = llm_file
        self.json_file = json_file
        self.summerizer = pipeline("summarization")
        self.llm : Llama = None
        self.sum_min = sum_min
        self.sum_max = sum_max
        # input_gen_config = generation_config_()

    def load_models_json(self) -> Dict:
        file = self.json_file 
        with open(file, "r") as file_:
            model_db_json = json.loads(file_)
        return model_db_json

    def load_model_bin(self):
        self.llm = Llama(model_path = self.model_bin, verbose=False)
        
    def summerize(self, model_descr : str = None) -> str:
        summerized_ = self.summerizer(model_descr, min_length = self.sum_min, max_length = self.sum_max)        
        return " ".join(summerized_["generated_text"])
    
    # ToDO try configs.__init__ args for input and output descriptions

    def create_db(self) -> 'Model_DB':
        return self

    
llm = Llama(model_path="./models/ggml-model-f16.bin", verbose=False)

model_descr = "This is model: It maps sentences & paragraphs to a 768 dimensional dense vector space."

output = llm._create_completion(
    f"if we have a model description: {model_descr}.\n input describtion: ",
    max_tokens=3 * len(model_descr.split(" ")),
    temperature=0.7,  # 0.7 output
    top_p=0.8,  # 0.8 output
    top_k=10,  # 10 output
)

print(list(output)[0]["choices"][0]["text"].split("\n")[0])
