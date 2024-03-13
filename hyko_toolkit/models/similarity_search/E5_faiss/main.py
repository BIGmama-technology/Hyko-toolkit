from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents.base import Document
from metadata import Inputs, Outputs, Params, StartupParams, func


@func.on_startup
async def load(startup_params: StartupParams):
    global embeddings
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    The function retrieves relevant documents based on a similarity score threshold and returns them as output.
    Args:
        inputs (Inputs): Input data containing the text to be processed.
        params (Params): Parameters for the function, including the score threshold and top k results.

    Returns:
        Outputs: Processed text containing relevant documents based on the similarity score threshold.
    """
    docs = inputs.docs
    lang_docs = [Document(page_content=i) for i in docs]
    db = FAISS.from_documents(documents=lang_docs, embedding=embeddings)
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "score_threshold": params.score_threshold,
            "k": params.top_k,
        },
    )
    relevant_documents = retriever.invoke(inputs.query)
    relevant_documents = [i.page_content for i in relevant_documents]
    return Outputs(result=relevant_documents)
