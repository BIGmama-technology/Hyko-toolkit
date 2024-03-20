"""register all apis"""

### Openai API
from .anthropic.chat.metadata import func as func
from .cohere.chat.metadata import func as func  # noqa: F811
from .cohere.text_embedding.metadata import func as func  # noqa: F811
from .gemini.chat.metadata import func as func  # noqa: F811
from .openai.text_completion.metadata import func as func  # noqa: F811
from .openai.text_embedding.metadata import func as func  # noqa: F811
