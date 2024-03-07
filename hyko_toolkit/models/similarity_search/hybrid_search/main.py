from langchain.retrievers import BM25Retriever, EnsembleRetriever
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
    Perform Hybrid Search on a list of documents based on a given query.
    Args:
        bm25_k : Number of top results to consider in Best Matching Algorithm (BM25).
        faiss_k : Number of top results to consider in Similarity Search Algorithm.
    Returns:
        Outputs: Processed text containing relevant documents based on the hybrid search.
    """
    docs = inputs.docs
    lang_docs = [Document(page_content=i) for i in docs]
    # BM25
    bm25_retriever = BM25Retriever.from_documents(lang_docs)
    bm25_retriever.k = params.bm25_k
    # Similarity Search
    faiss_vectorstore = FAISS.from_documents(documents=lang_docs, embedding=embeddings)
    faiss_retriever = faiss_vectorstore.as_retriever(
        search_kwargs={"k": params.faiss_k}
    )
    # Hybrid Search
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
    )
    relevant_documents = ensemble_retriever.get_relevant_documents(inputs.query)
    relevant_documents = [i.page_content for i in relevant_documents]
    return Outputs(result=relevant_documents)
