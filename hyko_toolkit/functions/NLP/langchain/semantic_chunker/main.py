from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from metadata import Inputs, Outputs, Params, StartupParams, func


@func.on_startup
async def load(startup_params: StartupParams):
    global embeddings
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    This function processes the input text using a SemanticChunker tool to split it into semantic chunks
    based on predefined embeddings.

    Args:
        inputs (Inputs): Input data containing the text to be processed.
        params (Params): Parameters for the function (not used in this function).

    Returns:
        Outputs: Processed text with semantic chunks separated and labeled.
    """
    text_splitter = SemanticChunker(embeddings)
    docsdocs = text_splitter.create_documents([inputs.text])
    page_contents = []
    for i, text in enumerate(docsdocs):
        sep = f"\n<<-- Part {i+1} -->>\n"
        page_contents.append(f"{sep}\n{text.page_content}")
    output = " ".join(page_contents)
    return Outputs(result=output)
