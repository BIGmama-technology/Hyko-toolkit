from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore

from .metadata import Inputs, Outputs, Params, func


@func.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    This function processes the input text using a RecursiveCharacterTextSplitter
    to split it into chunks based on specified parameters.

    Args:
        inputs (Inputs): Input data containing the text to be processed.
        params (Params): Parameters for the function, including chunk size and overlap.

    Returns:
        Outputs: Processed text with chunks separated and labeled.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=params.chunk_size,
        chunk_overlap=params.chunk_overlap,
        length_function=len,
        is_separator_regex=True,
    )
    chunks = text_splitter.create_documents([inputs.text])
    text_chunks = [chunk.page_content for chunk in chunks]
    return Outputs(chunks=text_chunks)
