"""register all apis"""

### Openai API
from .arxiv.articles_lookup.metadata import func as func
from .google.urls_lookup.metadata import func as func  # noqa: F811
from .mediawiki.text_lookup.metadata import func as func  # noqa: F811
from .openai.text_completion.metadata import func as func  # noqa: F811
from .openai.text_embedding.metadata import func as func  # noqa: F811
