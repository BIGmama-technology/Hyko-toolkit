"""register all apis"""

### Openai API
from .openai.text_completion.metadata import func as func
from .openai.text_embedding.metadata import func as func  # noqa: F811
from .stability_ai.text_to_image.metadata import func as func  # noqa: F811
