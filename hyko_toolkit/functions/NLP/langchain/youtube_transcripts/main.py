from langchain_community.document_loaders import YoutubeLoader
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Loads content from a YouTube video specified by the input URL and extracts relevant documents.
    The content can be loaded with optional language and translation parameters.
    The function returns the extracted content as output.

    Args:
        inputs (Inputs): Input data containing the YouTube video URL.
        params (Params): Parameters for the function, including language and translation settings.

    Returns:
        Outputs: Extracted content from the YouTube video.
    """
    loader = YoutubeLoader.from_youtube_url(
        inputs.url,
        add_video_info=False,
        language=[params.language],
        translation=params.translation,
    )
    documents = loader.load()
    relevant_documents = [i.page_content for i in documents]
    result = " ".join(relevant_documents)
    return Outputs(result=result)
