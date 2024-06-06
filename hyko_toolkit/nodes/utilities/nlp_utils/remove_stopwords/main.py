import nltk
from nltk.tokenize import word_tokenize

from .metadata import Inputs, Outputs, Params, node


@node.on_startup
async def startup(params: Params):
    nltk.download("punkt")
    nltk.download("stopwords")


@node.on_call
async def main(inputs: Inputs, params: Params) -> Outputs:
    """
    Remove stopwords from the text using the specified list of stopwords for the given language.

    Args:
    - text (str): The input text from which stopwords are to be removed.
    - language (str): Language of the stopwords .

    Returns:
    - str: The text with stopwords removed.
    """
    stopwords = set(nltk.corpus.stopwords.words(params.language))

    # Tokenize the text
    tokens = word_tokenize(inputs.text)

    # Remove stopwords
    filtered_tokens = [word for word in tokens if word.lower() not in stopwords]

    # Join the filtered tokens back into a single string
    filtered_text = " ".join(filtered_tokens)

    return Outputs(result=filtered_text)
