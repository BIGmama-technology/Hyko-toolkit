from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    This function processes the input text using a RecursiveCharacterTextSplitter tool
    to split it into chunks based on specified parameters. It then formats the chunks
    and concatenates them with separators, and returns the result.

    Args:
        inputs (Inputs): Input data containing the text to be processed.
        params (Params): Parameters for the function, including chunk size and overlap.

    Returns:
        Outputs: Processed text with chunks separated and labeled.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=params.chunk_size,
        chunk_overlap=params.chunk_overlap,
        length_function=len,
        is_separator_regex=True,
    )
    docsdocs = text_splitter.create_documents([inputs.text])
    page_contents = []
    for i, text in enumerate(docsdocs):
        sep = f"<<-- Part {i+1} -->>"
        page_contents.append(f"{sep}\n{text.page_content}")
    output = " ".join(page_contents)
    return Outputs(result=output)
