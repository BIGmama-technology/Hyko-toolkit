import gc
import io

import matplotlib.pyplot as plt
import numpy as np
from hyko_sdk.components import Ext
from hyko_sdk.io import Image
from metadata import Inputs, Outputs, Params, StartupParams, func
from transformers import pipeline


def show_mask(mask: np.ndarray, ax: plt.Axes, random_color: bool):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)  # I used imshow for writing mask_image on ax not for display.
    del mask
    gc.collect()


def show_masks_on_image(raw_image: np.ndarray, masks: list):
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.imshow(np.array(raw_image))
    ax.set_autoscale_on(False)
    for mask in masks:
        show_mask(mask, ax=ax, random_color=True)
    plt.axis("off")
    width, height = raw_image.size
    ax.set_xlim([0, width])
    ax.set_ylim([height, 0])
    plt.tight_layout()

    # Convert the plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close(fig)
    return buffer


def show_box(box: tuple, ax: plt.Axes):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(
        plt.Rectangle((x0, y0), w, h, edgecolor="green", facecolor=(0, 0, 0, 0), lw=2)
    )


def show_boxes_on_image(raw_image: np.ndarray, boxes: list):
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.imshow(raw_image)
    for box in boxes:
        show_box(box, ax)
    plt.axis("off")
    width, height = raw_image.size
    ax.set_xlim([0, width])
    ax.set_ylim([height, 0])
    plt.tight_layout()

    # Convert the plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close(fig)
    return buffer


@func.on_startup
async def load(startup_params: StartupParams):
    global generator

    model = startup_params.hugging_face_model
    device_map = startup_params.device_map
    generator = pipeline(
        "mask-generation",
        model=model,
        device_map=device_map,
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    image = await inputs.input_image.to_pil()
    image = image.convert("RGB")

    outputs = generator(
        image,
        mask_threshold=params.mask_threshold,
        points_per_batch=params.points_per_batch,
        pred_iou_thresh=params.pred_iou_thresh,
        output_bboxes_mask=True,
        output_rle_masks=True,
    )
    bounding_boxes = outputs["bounding_boxes"]
    masks = outputs["masks"]
    box_image_buffer = show_boxes_on_image(image, bounding_boxes)
    masks_image_buffer = show_masks_on_image(image, masks)
    return Outputs(
        bbox_img=await Image(
            obj_ext=Ext.PNG,
        ).init_from_val(val=box_image_buffer.getvalue()),
        mask_img=await Image(
            obj_ext=Ext.PNG,
        ).init_from_val(
            val=masks_image_buffer.getvalue(),
        ),
    )
