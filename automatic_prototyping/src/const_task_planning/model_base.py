r"""
This file implements field-completion using 7B-Llama, loads model_db as json generates input and output describtions for each model
and stores everything in a JSON file as model_metadata Database

TODO: Implement Model_db_class using custom generation_config_ for input_description and output_description

get_func:
"""

from llama_cpp import Llama
import lmql
from pathlib import Path
from transformers import pipeline
from typing import Any, Optional, List, Dict
import json

MODEL_JSON_FILE_PATH = Path("../../data")
LLM_MODEL_BIN_PATH = Path("/home/lotfi/llama/models/7B")


class generation_config_:
    r"""
    class for Llama generation configuration
    """

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

    @property
    def get_kwargs(self) -> Dict:
        r"""
        get_kwargs:
            return: Dict, storing kwargs as keys and their values
        """
        generation_args = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        ]

        attr_dict = dict()
        for attr_name in generation_args:
            attr_value = getattr(self, attr_name)
            attr_dict.update({attr_name: attr_value})

        del generation_args
        return attr_dict


class Model_DB:
    r"""
    Implemets Model Database class:
        Model_db_dict : Dictionary storing model, input, and output describtions/model as keys
                    their corresponding values (contains only models from the huggingface hub for now)
    """
    model_db_dict: Dict = dict()

    def __init__(
        self,
        json_file: str = "model_id_descr_map.json",
        llm_file: str = "ggml-model-f16.bin",
        summerizer_model: str = None,
        sum_min: int = 5,
        sum_max: int = 10,
    ):
        # "./models/ggml-model-f16.bin"
        self.model_bin = "./" + str(LLM_MODEL_BIN_PATH / llm_file)
        self.json_file = MODEL_JSON_FILE_PATH / json_file
        self.summerizer = pipeline(
            "summarization"
        )  # add variations for different Sum-models
        self.llm: Llama = None
        self.sum_min = sum_min
        self.sum_max = sum_max

    def load_models_json(self) -> Dict:
        r"""
        loads model metadata from cached JSON file
        """
        file = self.json_file
        with open(file, "r") as file_:
            model_db_json = json.load(file_)
        return model_db_json

    def load_model_bin(self):
        r"""
        Loads LLM-model weights (Meta's Llama for now)
        """
        self.llm = Llama(model_path=self.model_bin, verbose=False)

    def summerize(
        self, model_descr: str = None, max_length: int = 512, min_length: int = None
    ) -> str:
        r"""
        Normalizes model-description through summerization.
        TODO: consider llama.ctx = 512 = prompt(summerized) + Generated(max)
        """

        model_descr = model_descr.strip()
        model_descr_size = len(model_descr.split(" "))

        if model_descr_size < max_length:
            model_descr = model_descr
        else:
            model_descr = " ".join(model_descr.split(" ")[:max_length])

        try:
            summerized_ = self.summerizer(
                model_descr, min_length=self.sum_min, max_length=model_descr_size / 2
            )

        except Exception as e:
            print(f"Exception: {e}")
            summerized_ = model_descr

        if isinstance(summerized_, str):
            return summerized_
        else:
            return summerized_[0]["summary_text"]

    def get_input_describtion(self, llm: Llama = None, model_descr: str = None) -> str:
        r"""
        Get input describtion from model_describtion
        """
        try:
            model_descr = self.summerize(model_descr)
        except Exception as e:
            print(e)
            pass
        if len(model_descr.split(" ")) >= self.sum_max:
            model_descr = " ".join(model_descr.split(" ")[: self.sum_max])
        else:
            pass

        input_descr = llm._create_completion(
            f"if we have a model description: {model_descr}.\n input describtion: ",
            max_tokens=5,
            temperature=0.7,  # 0.7 output
            top_p=0.8,  # 0.8 output
            top_k=10,  # 10 output
        )
        input_descr = list(input_descr)[0]["choices"][0]["text"].split("\n")[0]
        return input_descr

    def get_output_describtion(self, llm: Llama, model_descr: str = None) -> str:
        r"""
        get output describtion
        """
        try:
            model_descr = self.summerize(model_descr)
        except Exception as e:
            print(e)
            pass

        output_descr = llm._create_completion(
            f"if we have a model description: {model_descr}.\n output describtion: ",
            max_tokens=3,
            temperature=0.7,  # 0.7 output
            top_p=0.8,  # 0.8 output
            top_k=10,  # 10 output
        )
        print(list(output_descr))
        print()
        print()

        try:
            output_descr = list(output_descr)[0]["choices"][0]["text"].split("\n")[0]
            return output_descr
        except Exception as e:
            return output_descr

    def create_db(self) -> "Model_DB":
        self.load_model_bin()
        model_db_json = self.load_models_json()

        for model_id, model_descrb in zip(
            model_db_json["models"].keys(), model_db_json["models"].values()
        ):
            model_descr = self.summerize(model_descrb)

            input_describtion = self.get_input_describtion(
                model_descr=model_descr, llm=self.llm
            )
            output_describtion = self.get_output_describtion(
                model_descr=model_descr, llm=self.llm
            )

            self.model_db_dict.update(
                {
                    model_id: {
                        "model_descr": model_descr,
                        "input_descr": input_describtion,
                        "output_descr": output_describtion,
                    }
                }
            )


# model_db = Model_DB()
# model_db.create_db()
# print(model_db.model_db_dict)

DEBUG = True

if DEBUG:
    llm = Llama(
        model_path="/home/lotfi/llama/models/13B/ggml-model-f16.bin",
        verbose=False,
        n_ctx=1024,
    )
    print("Loaded model ---- ")

    model_descr = "This is model: It maps sentences & paragraphs to a 768 dimensional dense vector space."
    model_descr_0 = (
        "take advantage of artificial intelligence to improve the driving experience."
    )
    input_descr = "Sentences or paragraphs"
    output_descr = "768 dimensional dense vectors"
    question = "How to reduce fuel consumption?"
    prompt = f"<Raw Problem> : <START>{model_descr_0} <END>.\n <Technical problems>:  "
    # bytes_ = prompt.encode("utf-8")
    # print(type(bytes_.__len__()))

    output = llm._create_completion(
        prompt,
        max_tokens=512 - len(llm.tokenize(prompt.encode("utf-8"))),
        temperature=0.9,  # 0.7 output
        top_p=0.6,  # 0.8 output
        top_k=2,  # 10 output
    )

    print(list(output))
    # print(list(output)[0]["choices"][0]["text"].split("\n")[0])
    # print(list(output)[0])
