import numpy as np
import torch
from pydantic import Field
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from hyko_sdk.function import SDKFunction
from hyko_sdk.metadata import CoreModel

func = SDKFunction(
    description="Takes a list of strings and a query and returns the top K most similar sentences to the query",
    requires_gpu=False,
)


@func.on_startup
async def init():
    global model
    model = SentenceTransformer(
        "all-MiniLM-L6-v2", device="cuda:0" if torch.cuda.is_available() else "cpu"
    )


class Inputs(CoreModel):
    sentences: list[str] = Field(..., description="List of sentences to search in")


class Params(CoreModel):
    query: str = Field(..., description="Query string")
    top_k: int = Field(default=5, description="Number of sentences to output")


class Outputs(CoreModel):
    selected_sentences: list[str] = Field(
        ..., description="List of top k elected sentences"
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
