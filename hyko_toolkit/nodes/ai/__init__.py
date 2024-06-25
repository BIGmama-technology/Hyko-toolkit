# Register Models

"""register all apis"""

from .audio_huggingface.metadata import node as node  # noqa: F811
from .background_image_removal.metadata import node as node  # noqa: F811
from .computer_vision_huggingface.metadata import node as node  # noqa: F811
from .computer_vision_ultralytics.metadata import node as node  # noqa: F811
from .elevenlabs.metadata import node as node  # noqa: F811
from .elevenlabs.speech_to_speech.metadata import node as node  # noqa: F811
from .elevenlabs.text_to_speech.metadata import node as node  # noqa: F811
from .gemini.vision.metadata import node as node  # noqa: F811
from .llms.metadata import llm_node as llm_node
from .mutlimodal_huggingface.metadata import node as node  # noqa: F811
from .nlp_huggingface.metadata import node as node  # noqa: F811
from .ocr.metadata import node as node  # noqa: F811
from .openai.metadata import node as node  # noqa: F811
from .replicate.metadata import node as node  # noqa: F811
from .stability_ai.metadata import node as node  # noqa: F811
