from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents.base import Document
from metadata import Inputs, Outputs, Params, func

from hyko_sdk.models import CoreModel


@func.on_startup
async def load(startup_params: CoreModel):
    global embeddings
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Document compressor that uses embeddings to drop documents unrelated to the query.
    Args:
        query (str): (Query or the Question to compare against the input text)
        docs (list[str]): Docs (Text Input) .
        embeddings_similarity_threshold (float): Query or the Question to compare against the input text.
        score_threshold (float): Threshold score to filter similarity results.
        top_k (int) : Number of top results to consider .
    Returns:
        result (list[str]): Top K results
    """
    docs = inputs.docs
    embeddings_filter = EmbeddingsFilter(
        embeddings=embeddings,
        similarity_threshold=params.embeddings_similarity_threshold,
    )
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
        base_compressor=embeddings_filter, base_retriever=retriever
    )
    relevant_documents = compression_retriever.get_relevant_documents(inputs.query)
    relevant_documents = [i.page_content for i in relevant_documents]
    return Outputs(result=relevant_documents)
