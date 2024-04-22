"""register all apis"""

from .anthropic.chat.metadata import func as func
from .arxiv.articles_lookup.metadata import func as func  # noqa: F811
from .cohere.chat.metadata import func as func  # noqa: F811
from .cohere.text_embedding.metadata import func as func  # noqa: F811
from .elevenlabs.speech_to_speech.metadata import func as func  # noqa: F811
from .elevenlabs.text_to_speech.metadata import func as func  # noqa: F811
from .gemini.chat.metadata import func as func  # noqa: F811
from .gemini.text_embedding.metadata import func as func  # noqa: F811
from .gemini.vision.metadata import func as func  # noqa: F811
from .google.text_lookup.metadata import func as func  # noqa: F811
from .groq.chat.metadata import func as func  # noqa: F811
from .huggingface.chat.metadata import func as func  # noqa: F811
from .mistral_ai.text_completion.metadata import func as func  # noqa: F811
from .mistral_ai.text_embedding.metadata import func as func  # noqa: F811
from .openai.speech_to_text.metadata import func as func  # noqa: F811
from .openai.text_completion.metadata import func as func  # noqa: F811  # noqa: F811
from .openai.text_embedding.metadata import func as func  # noqa: F811
from .openai.text_to_speech.metadata import func as func  # noqa: F811
from .openai.vision.metadata import func as func  # noqa: F811
from .openrouter.chat.metadata import func as func  # noqa: F811
from .serpapi.bing.metadata import func as func  # noqa: F811
from .serpapi.duckduckgo.metadata import func as func  # noqa: F811
from .stability_ai.image_to_image_with_a_mask.metadata import func as func  # noqa: F811
from .stability_ai.image_to_image_with_prompt.metadata import func as func  # noqa: F811
from .stability_ai.image_to_video.metadata import func as func  # noqa: F811
from .stability_ai.image_upscaler.metadata import func as func  # noqa: F811
from .stability_ai.text_to_image.metadata import func as func  # noqa: F811
from .tune_studio.text_completion.metadata import func as func  # noqa: F811
from .wikimedia.text_lookup.metadata import func as func  # noqa: F811
