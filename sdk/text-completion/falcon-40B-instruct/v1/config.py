from pydantic import Field
from hyko_sdk import extract_metadata, CoreModel

description = "instruct generation model"

class Inputs(CoreModel):
    prompt : str = Field(..., description="User prompt to falcon-instruct")

class Params(CoreModel):
    system_prompt : str = Field(default=None, description = "system-prompt or system-instruction to falcon-instruct")
    max_length : int = Field(default = 200, description= "Max tokens to generate")
    top_k : int = Field(default=10,description="top_k candidates for each token generation")
    temperature: float = Field(default=0.6, description="Temperature of falcon")
    top_p: float = Field(default=0.6, description="Top P of falcon")

class Outputs(CoreModel):
    generated_text : str = Field(..., description="Generated Text from falcon-instruct")

if __name__ == "__main__":
    extract_metadata(
                    Inputs, Params, Outputs,  # type: ignore
                    description, False
                )