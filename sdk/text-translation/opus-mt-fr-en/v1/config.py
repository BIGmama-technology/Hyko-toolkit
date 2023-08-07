from pydantic import  Field
from hyko_sdk import extract_metadata, CoreModel

description = "OPUS French to English Translation specialized model"

class Inputs(CoreModel):
    french_text: str = Field(..., description="French text")

class Params(CoreModel):
    pass

class Outputs(CoreModel):
    english_translated_text: str = Field(..., description="English translated text")

if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )