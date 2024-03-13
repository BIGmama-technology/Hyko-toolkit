import re

from metadata import Inputs, Outputs, Params, func


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Remove special characters and punctuation from the text, keeping only alphanumeric characters and spaces.

    Args:
    - text (str): The input text from which special characters and punctuation will be removed.

    Returns:
    - str: The text with special characters and punctuation removed.
    """
    # Define the regular expression pattern to match non-alphanumeric characters (excluding spaces)
    pattern = r"[^a-zA-Z0-9\s]"

    # Replace non-alphanumeric characters with an empty string
    cleaned_text = re.sub(pattern, "", inputs.text)

    return Outputs(result=" ".join(cleaned_text.strip().split()))
