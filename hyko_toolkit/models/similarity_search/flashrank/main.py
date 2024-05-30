from hyko_sdk.models import CoreModel
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents.base import Document

from .metadata import Inputs, Outputs, Params, func


@func.on_startup
async def load(startup_params: CoreModel):
    global embeddings
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    A tool employing re-ranking capabilities for enhancing search and retrieval pipelines, leveraging state-of-the-art cross-encoders.
    Args:
        inputs (Inputs): Input data containing the text to be processed.
        params (Params): Parameters for the function, including the score threshold and top k results.

    Returns:
        Outputs: Processed text containing relevant documents based on the similarity score threshold.
    """
    compressor = FlashrankRerank()
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
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )
    relevant_documents = compression_retriever.get_relevant_documents(inputs.query)
    relevant_documents = [i.page_content for i in relevant_documents]
    return Outputs(result=relevant_documents)
