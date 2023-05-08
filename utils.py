"""
Utility functions for model-selection using semantic + beam search
"""

from sentence_transformers import SentenceTransformer
import torch.nn as nn
from torch.types import _TensorOrTensors
from typing import Dict, List, Union
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

    def embed_model_metadata(self, metadata_db : List[MetaData], 
                             target_attr : List[str],
                             output_tensor : bool = True,
                             output_ndarray : bool = False,
                             ) -> Union[List[np.ndarray], List[_TensorOrTensors]]:
        r"""
        embed_model_db: Takes a model_metadata database, embeds relevant dict_values
        argmuents:
            model_name : str holding  the name of the embedding module used
        output:
            List[np.ndarray] : a List containing numpy.array(s) or torch.tensor(s) of the 
            corresponding model representative embedding(s)
        """

        # Iterate over the dict_list

        for i, MetaData_ in enumerate(metadata_db):
            
            description = MetaData_.description
            input_descr = MetaData_.inputs_descr
            output_descr = MetaData_.outputs_descr


    def embed_tasks(self, metadata_db : List[Dict],
                    target_attr : List[str] = None) -> Union[List[np.ndarray], List[_TensorOrTensors]]:
        
        r"""
        embed_tasks:  
        """
        pass

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