# Register Models

"""register all apis"""
from .audio_huggingface.speech_to_text.metadata import (
    func as func,  # noqa: F811
)
from .audio_huggingface.text_to_speech.metadata import func as func  # noqa: F811
from .background_image_removal.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_huggingface.depth_estimation.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_huggingface.image_classification.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_huggingface.image_segmentation.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_huggingface.mask_generation.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_huggingface.object_detection.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_huggingface.video_classification.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_huggingface.zero_shot_image_classification.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_ultralytics.image_classification.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_ultralytics.image_instance_segmentation.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_ultralytics.image_obb_object_detection.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_ultralytics.image_object_detection.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_ultralytics.image_pose_estimation.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_ultralytics.video_instance_segmentation.metadata import (
    func as func,  # noqa: F811  # noqa: F811
)
from .computer_vision_ultralytics.video_obb_object_detection.metadata import (
    func as func,  # noqa: F811
)
from .computer_vision_ultralytics.video_object_detection.metadata import (
    func as func,  # noqa: F811
)
from .elevenlabs.speech_to_speech.metadata import func as func  # noqa: F811
from .elevenlabs.text_to_speech.metadata import func as func  # noqa: F811
from .gemini.vision.metadata import func as func  # noqa: F811
from .llms.metadata import llm_node as llm_node
from .mutlimodal_huggingface.image_to_text.metadata import func as func  # noqa: F811
from .mutlimodal_huggingface.text_to_image.metadata import func as func  # noqa: F811
from .mutlimodal_huggingface.visual_question_answering.metadata import (
    func as func,  # noqa: F811
)
from .nlp_huggingface.fill_mask.metadata import func as func  # noqa: F811
from .nlp_huggingface.question_answering.metadata import (
    func as func,  # noqa: F811
)
from .nlp_huggingface.summarization.metadata import (
    func as func,  # noqa: F811  # noqa: F811
)
from .nlp_huggingface.text_classification.metadata import (
    func as func,  # noqa: F811  # noqa: F811
)
from .nlp_huggingface.text_generation.metadata import (
    func as func,  # noqa: F811
)
from .nlp_huggingface.translation.metadata import func as func  # noqa: F811
from .nlp_huggingface.zero_shot_classification.metadata import (
    func as func,  # noqa: F811
)
from .ocr.easyocr.metadata import func as func  # noqa: F811
from .ocr.surya_ocr.metadata import func as func  # noqa: F811
from .ocr.tesseract_ocr.metadata import (
    func as func,  # noqa: F811
)
from .openai.metadata import node as node  # noqa: F811
from .replicate.image_restoration.metadata import func as func  # noqa: F811
from .replicate.text_to_video.metadata import func as func  # noqa: F811
from .replicate.transcribe_speech.metadata import func as func  # noqa: F811
from .replicate.upscale_images.metadata import func as func  # noqa: F811
from .replicate.vision_models.metadata import func as func  # noqa: F811
from .stability_ai.image_to_image_with_a_mask.metadata import func as func  # noqa: F811
from .stability_ai.image_to_image_with_prompt.metadata import func as func  # noqa: F811
from .stability_ai.image_to_video.metadata import func as func  # noqa: F811
from .stability_ai.image_upscaler.metadata import func as func  # noqa: F811
from .stability_ai.text_to_image.metadata import func as func  # noqa: F811
