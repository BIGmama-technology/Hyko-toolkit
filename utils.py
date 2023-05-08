"""
Utility functions for model-selection using semantic + beam search
"""

from sentence_transformers import SentenceTransformer
import torch.nn as nn
from torch.types import _TensorOrTensors
from typing import Dict, List
import numpy as np
from functions.math.add.main import MetaData

class Embdder(nn.Module):
    r"""
    Embdder class: serves as a holistic container for the model_database representations,
                    and a iput_name":id},nput_query channel through which the semantic-search
                    is performed on the model_database
    """
    model_db : Dict = None
    def __init__(self, model_name: str = 'multi-qa-MiniLM-L6-cos-v1'):
        self.sent_bi_encoder = SentenceTransformer(model_name)
        self.model_db = None
        if not model_name:
            raise ValueError("model_name must be specified")

    def embed_model_db(model_metadata_db : List[MetaData] = None) -> List[np.ndarray]:
        r"""
        embed_model_db: Takes a model database, embeds relavent values from model_md_dicts
        argmuents:
            model_name : str holding  the name of the embedding module used
        output:
            List[np.ndarray] : a List containing numpy.array(s) or torch.tensor(s) of the 
            corresponding model representative embedding(s)
        """

        # Iterate over the dict_list

        '''
        [{"id": task_id, "task": task_name(str),
        "task_description":task_description(str), 
        "dep": dependency_task_id(List[int]), 
        "args": [{"input_type":type(str), "input_description":desc(str),
                                 "input_name":id},{..}]
        }, {..} ...]
        '''

        for i, MetaData_ in enumerate(model_metadata_db):

            
        



    def forward(
        self,
        output_numpy: bool = False,
        output_tensor: bool = True,
        model_db: Dict = None,
    ):
        if output_numpy == output_tensor:
            raise ValueError("Only one of output_numpy and output_tensor can be True")
        else: 
            pass
            
        if not model_db:
            raise ValueError("Model DataBase must be specified")
        

        pass