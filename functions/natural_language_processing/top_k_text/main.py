import numpy as np
import torch
from metadata import Inputs, Outputs, Params, func
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@func.on_startup
async def init():
    global model
    model = SentenceTransformer(
        "all-MiniLM-L6-v2", device="cuda:0" if torch.cuda.is_available() else "cpu"
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    global model

    # Encode the query and corpus sentences
    query_embedding = model.encode(
        [params.query], batch_size=100, show_progress_bar=True, convert_to_numpy=True
    )[0]
    corpus_embeddings = model.encode(
        inputs.sentences, batch_size=100, show_progress_bar=True, convert_to_numpy=True
    )
    similarity_scores = cosine_similarity([query_embedding], corpus_embeddings)[0]
    sorted_indices = np.argsort(similarity_scores)[::-1]

    return Outputs(
        selected_sentences=[inputs.sentences[i] for i in sorted_indices[: params.top_k]]
    )
