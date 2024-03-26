"""register all apis"""

### Openai API
from .anthropic.chat.metadata import func as func
from .arxiv.articles_lookup.metadata import func as func  # noqa: F811
from .cohere.chat.metadata import func as func  # noqa: F811
from .cohere.text_embedding.metadata import func as func  # noqa: F811
from .gemini.chat.metadata import func as func  # noqa: F811
from .gemini.text_embedding.metadata import func as func  # noqa: F811
from .google.text_lookup.metadata import func as func  # noqa: F811
from .groq.chat.metadata import func as func  # noqa: F811
from .huggingface.chat.metadata import func as func  # noqa: F811
from .openai.text_completion.metadata import func as func  # noqa: F811  # noqa: F811
from .openai.text_embedding.metadata import func as func  # noqa: F811
from .openrouter.chat.metadata import func as func  # noqa: F811
from .serpapi.bing.metadata import func as func  # noqa: F811
from .serpapi.duckduckgo.metadata import func as func  # noqa: F811
from .wikimedia.text_lookup.metadata import func as func  # noqa: F811
