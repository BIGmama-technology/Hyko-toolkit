from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
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
        sep = f"\n<<-- Part {i+1} -->>\n"
        page_contents.append(f"{sep}\n{text.page_content}")
    output = " ".join(page_contents)
    return Outputs(result=output)
