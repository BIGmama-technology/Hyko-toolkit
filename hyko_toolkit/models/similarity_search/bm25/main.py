from langchain.retrievers import BM25Retriever
from langchain_core.documents.base import Document
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Perform BM25 retrieval on a list of documents based on a given query.

    Args:
        inputs (list[str]): An object containing input documents and query.
        top_k (int): Number of top results to consider.
    Returns:
        Outputs: An object containing relevant document contents.
    """
    docs = inputs.docs
    lang_docs = [Document(page_content=i) for i in docs]
    retriever = BM25Retriever.from_documents(lang_docs)
    retriever.k = params.top_k
    relevant_documents = retriever.invoke(inputs.query)
    relevant_documents = [i.page_content for i in relevant_documents]
    return Outputs(result=relevant_documents)
