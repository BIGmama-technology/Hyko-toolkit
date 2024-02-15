from langchain_community.document_loaders import YoutubeLoader
from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
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
