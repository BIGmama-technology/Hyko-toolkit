"""
Utility functions for model-selection using semantic + beam search
"""

import torch 
import torch.nn as nn
from torch.types import _TensorOrTensors
import numpy as np
from sentence_transformers import SentenceTransformer, util
from const_task_planning.task_planning import TaskPlan
from src.utils.utils import MetaData
from typing import Dict, List, Union, Tuple, Optional

DEBUG = False

class Embedder(nn.Module):
    r"""
    Embdder class: Holistic embbeding module for both model and tasks metadata databases.
    """
    model_db: Dict = None
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        super().__init__()
        self.sent_bi_encoder = SentenceTransformer(model_name)
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
        target_attr: List[str]=[],
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
            model_embed = self.encode_(MetaData_)
            
            '''{
                "description_embed": self.encode_(MetaData_["description"]),
                "inputs_embed": self.encode_(MetaData_["input_desc"]),
                "outputs_embed": self.encode_(MetaData_["output_desc"]),
            }'''

            model_db_embeds.append(model_embed)

        return model_db_embeds

    def embed_task(
        self, task_plan : TaskPlan = None, target_attr: List[str] = []
    ) -> Union[List[np.ndarray], List[_TensorOrTensors]]:
        r"""
        Docstring ...
        """
        # iterate over the task metadata database
        task_db_embeds = []
        for MetaData_ in task_plan.task_plan_:
            task_embed =  self.encode_(MetaData_)
            task_db_embeds.append(task_embed)

        return task_db_embeds

    def forward(
        self,
        output_numpy: bool = False,
        output_tensor: bool = True,
        model_db: List[MetaData] = None,
        task_db: List[Dict] = None,
    ) -> Tuple[Union[List[np.ndarray], List[_TensorOrTensors]],
               Union[List[np.ndarray], List[_TensorOrTensors]]]:
        r"""
        Embedder module forward function override.
        """

        if output_numpy == output_tensor:
            raise ValueError("Only one of output_numpy and output_tensor can be True")

        if not model_db:
            raise ValueError("Model DataBase must be specified")

        if not task_db:
            raise ValueError("Tasks DataBase must be specified")

        model_db_embeds = self.embed_model_metadata(model_db)
        task_db_embeds = self.embed_task(task_db)

        return model_db_embeds, task_db_embeds

class SemanticSearchEngine(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedder = Embedder()

    def similarity_measure(self, model_db : List[MetaData],
                                 task_db : List[Dict],
                                 top_k : int = 5):
        
        r"""
        similarity_measure : measures Cross Semantic Textual Similarity between model_db_embeds
                             and task_db_embeds.
                             args: model_db_embeds : List[Union[np.ndarray, torch.Tensor]]
                                   task_db_embeds : List[Union[np.ndarray, torch.Tensor]

                             outputs: List of node_candidates at each task (task-planner output item)
        """

        # embed model and task dbases
        model_db_embeds, task_db_embeds = self.embedder(model_db = model_db,
                                                        task_db = task_db)
    
        # Iterate over model_base_embed and apply semantic search for each Query(task_embed)
        top_k = min(top_k, len(model_db_embeds))

        node_wise_cand_idx = [] # list for model candidates at each sequential task
        for task_embed in task_db_embeds:
            description_sim_scores = torch.tensor([util.cos_sim(task_embed, model_embed["description_embed"])[0] for model_embed in model_db_embeds])
            # input_descr_sim_scores =torch.tensor([util.cos_sim(task_embed['inputs_embed'], model_embed["inputs_embed"])[0] for model_embed in model_db_embeds])
            # output_descr_sim_scores = torch.tensor([util.cos_sim(task_embed['outputs_embed'], model_embed["outputs_embed"])[0] for model_embed in model_db_embeds])
            
            # score weighted average
            avg_tens = description_sim_scores

            candidates = torch.topk(avg_tens, k = top_k)[1] # [1] for idx
            node_wise_cand_idx.append(candidates)
            if DEBUG:
                print(type(candidates)) # Debugging

        return node_wise_cand_idx
    
    def forward(self, model_db : List[MetaData], task_db : List[Dict]) -> List[int]:
        
        model_id_list : List[Optional[int]] = [MetaData_["id"] for MetaData_ in model_db]

        node_wise_cand_idx = self.similarity_measure(model_db, task_db)

        node_wise_cand_ids = []

        for idx_list in node_wise_cand_idx:
            cand_ids = np.array(model_id_list)[idx_list]
            node_wise_cand_ids.append(cand_ids.tolist())

        return node_wise_cand_ids