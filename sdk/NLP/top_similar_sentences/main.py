import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
from hyko_sdk import SDKFunction
from pydantic import Field, BaseModel
func = SDKFunction(
    "",
    True,
)

class Inputs(BaseModel):
    pass

#Parameters to the function
class Params(BaseModel):
    first : list[str] = Field(..., description = "search_documents")
    second : str = Field(..., description = "query")
    third : int = Field(default = 5, description = "top_k")

#Outputs of the function
class Outputs(BaseModel):
    output : list[str]= Field(..., description= "list of top elected sentences")


model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda:0')

@func.on_execute
async def main(inputs : Inputs, params : Params) -> Outputs: 
  
    # Encode the query and corpus sentences
    query_embedding = model.encode([params.second], batch_size = 100, show_progress_bar = True, convert_to_numpy= True)[0]
    corpus_embeddings = model.encode(params.first,  batch_size = 100, show_progress_bar = True, convert_to_numpy= True)
    similarity_scores = cosine_similarity([query_embedding], corpus_embeddings)[0]
    sorted_indices = np.argsort(similarity_scores)[::-1]
    top_similar_sentences = [params.first[i] for i in sorted_indices[:params.third]]
    return  Outputs(output=top_similar_sentences)
    
