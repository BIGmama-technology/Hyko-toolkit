"""register all apis"""

from .arxiv.articles_lookup.metadata import func as func
from .google.text_lookup.metadata import func as func  # noqa: F811
from .openai.text_completion.metadata import func as func  # noqa: F811
from .openai.text_embedding.metadata import func as func  # noqa: F811
from .serpapi.bing.metadata import func as func  # noqa: F811
from .serpapi.duckduckgo.metadata import func as func  # noqa: F811
from .wikimedia.text_lookup.metadata import func as func  # noqa: F811
