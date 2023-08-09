from fastapi import FastAPI
from config import Inputs, Params, Outputs
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sentence_tranformers import SentenceTransformer
from numpy import np

#################################################################
app = FastAPI()

# Insert the main code of the function here #################################################################

@app.post(
    "/load",
    response_model=None,
)
def load():
    pass


@app.post(
    "/",
    response_model=Outputs,
)


async def maint(inputs : Inputs, params : Params):
    model = SentenceTransformer('bert-base-uncased')

    # Encode the query and corpus sentences
    query_embedding = model.encode([params.second])[0]
    corpus_embeddings = model.encode(params.first)
    similarity_scores = cosine_similarity([query_embedding], corpus_embeddings)[0]
    sorted_indices = np.argsort(similarity_scores)[::-1]
    top_similar_sentences = [params.first[i] for i in sorted_indices[:params.third]]
    return  Outputs(output=top_similar_sentences)
    
    









