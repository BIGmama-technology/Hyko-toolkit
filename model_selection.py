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
    Embdder class: Holistic embbeding module for both model and tasks metadata databases.
    """
    model_db: Dict = None

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.sent_bi_encoder = SentenceTransformer(model_name)
        self.model_db = None
        if not model_name:
            raise ValueError("model_name must be specified")

    def encode_(
        self,
        input_string: str = None,
        output_tensor: bool = True,
        output_ndarray: bool = False,
    ) -> Union[np.ndarray, _TensorOrTensors]:
        r"""
        Encodes string to corresponding embedding
        """
        output_embed = self.sent_bi_encoder.encode(
            sentences=input_string,
            convert_to_numpy=output_ndarray,
            convert_to_tensor=output_tensor,
        )
        return output_embed

    def embed_model_metadata(
        self,
        metadata_db: List[MetaData],
        target_attr: List[str],
        output_tensor: bool = True,
        output_ndarray: bool = False,
    ) -> Union[List[np.ndarray], List[_TensorOrTensors]]:
        r"""
        embed_model_db: Takes a model_metadata database, embeds relevant dict_values
        argmuents:
            model_name : str holding  the name of the embedding module used
        output:
            List[np.ndarray] : a List containing numpy.array(s) or torch.tensor(s) of the
            corresponding model representative embedding(s)
        """

        # Iterate over the model metadata list
        model_db_embeds = []

        for MetaData_ in metadata_db:
            model_embed = {
                "description_embed": self.encode_(MetaData_.description),
                "input_descr": self.encode_(MetaData_.inputs_descr),
                "outputs_descr": self.encode_(MetaData_.outputs_descr),
            }

            model_db_embeds.append(model_embed)

        return model_db_embeds

    def embed_task_metadata(
        self, metadata_db: List[Dict], target_attr: List[str] = None
    ) -> Union[List[np.ndarray], List[_TensorOrTensors]]:
        r"""
        Docstring ...
        """
        # iterate over the task metadata database
        task_db_embeds = []
        for MetaData_ in metadata_db:
            task_embed = {
                "description_embed": self.encode_(MetaData_["task_description"]),
                "input_descr": self.encode_(MetaData_["inputs"]["input_description"]),
                "output_descr": self.encode_(MetaData_["outputs"]["output_description"]),
            }
            task_db_embeds.append(task_embed)

        return task_db_embeds

    def forward(
        self,
        output_numpy: bool = False,
        output_tensor: bool = True,
        model_db: List[MetaData] = None,
        task_db: List[Dict] = None,
    ):
        r"""
        Embedder module forward function override.
        """

        if output_numpy == output_tensor:
            raise ValueError("Only one of output_numpy and output_tensor can be True")
        else:
            pass

        if not model_db:
            raise ValueError("Model DataBase must be specified")

        if not task_db:
            raise ValueError("Tasks DataBase must be specified")

        model_db_embeds = self.embed_model_metadata(model_db)
        task_db_embeds = self.embed_task_metadata(task_db)

        return model_db_embeds, task_db_embeds

class SemanticSearchEngine(nn.Module):
    def __init__(self):
        pass

    def similarity_measure(self):
        r"""
        similarity_measure : measures Cross Semantic Textual Similarity between model_db_embeds
                             and task_db_embeds.
                             args: model_db_embeds : List[Union[np.ndarray, torch.Tensor]]
                                   task_db_embeds : List[Union[np.ndarray, torch.Tensor]

                             outputs: Cross STS (Semantic Textual Similarity) Matrix (Union[torch.Tensor, np.ndarray])
        
        NOTE : Can use Semantic-Search or Elastic-Search from sentence-transformers
        """
        
        pass