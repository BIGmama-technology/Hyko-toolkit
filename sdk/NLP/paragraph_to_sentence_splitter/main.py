from fastapi import FastAPI
from config import Inputs, Params, Outputs
import nltk

app = FastAPI()

###################################################################################"""""

#the main code of the function
@app.post(
    "/load",
    response_model = None,
) 

def load(): 
    pass

# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.
@app.post(
    "/",
    response_model =Outputs,
)

async def main (inputs: Inputs, params : Params):
    sentences = nltk.sent_tokenize( params.first)
    return Outputs(output = sentences)
    





















# A parser that converts a paragraph to a list of sentences ( tokenization sentence_level )
import nltk 
from typing import List
nltk.download('punkt')
def paragraph_to_sentence_splitter ( paragraph : str) -> List[str] :
    sentences = nltk.sent_tokenize(paragraph)
    return sentences
