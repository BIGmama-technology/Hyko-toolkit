<!-- x-release-please-start-version -->
 ![Static Badge](https://img.shields.io/badge/Release-v2.0.0-/?style=flat&logo=track)
<!-- x-release-please-end -->

# Hyko toolkit

## Table of contents
- [Description](#description)
- [Toolkit components](#toolkit-components)
    - [Functions and Models](#functions-and-models)
    - [APIs](#apis)
- [Adding new function/model to the toolkit](#adding-new-functionmodel-to-the-toolkit)

## Description

[Hyko](https://hyko.ai) Toolkit stands as a robust repository housing a diverse collection of tools. From a curated selection of functions and APIs to state-of-the-art AI models, each component has been meticulously crafted to empower developers in constructing versatile blueprints effortlessly.


## Toolkit components

The Hyko Toolkit consists of three primary categories of components: **_functions_**, **_models_**, and **_APIs_**. Let's delve into functions and models first, as they share many similarities.

- <span id="functions-and-models">**_Functions_** and **_Models_**</span>: These are essentially FastAPI applications that define a specific set of inputs, parameters, and outputs. This metadata is crucial for both the Hyko frontend and backend to effectively utilize these functions and models. After defining the metadata, the FastAPI application is packaged and bundled into a Docker image. When executing a task involving a particular function or model, this Docker image is built on the local machine.

- <span id="apis">**_APIs_**</span>: Similar to functions and models, APIs also require inputs, parameters, and outputs to extract metadata. However, APIs differ in that they do not necessitate local execution on a computer. Therefore, there's no need for a Docker image or a FastAPI application. Instead, the Hyko backend makes requests to these external APIs. These APIs can range from OpenAI and Hugging Face inference APIs to OpenRouter APIs, and beyond.


## Adding new function/model to the toolkit

All components of the Hyko Toolkit functions, models, and APIs—are centralized within the `hyko_toolkit` directory. This directory is further organized into the aforementioned categories: functions, models, and apis. Within each category directory, a structured hierarchy based on tasks (e.g., downloaders, utils, computer vision) ensures systematic organization. To integrate a new tool into the toolkit, the following steps are essential:

- **Determine Task Placement**: 

    Choose the appropriate task category within which your tool aligns or create a new one if necessary.

- **Create Metadata File**:

    `metadata.py`: This file serves as a repository for essential metadata concerning your tool. Include details such as the types of inputs, parameters, and outputs it utilizes, along with a descriptive name, assigned task, and a broad overview of its functionality.

- **Develop Main Logic**:

    `main.py`: Here, encapsulate the core logic of your tool—the sequence of operations that occur upon execution of the function or model.

- **Add a Dockerfile for your tool**:

    `Dockerfile`: After finishing up with `metadata.py` and `main.py` file, the fastapi app needs to be packaged inside a docker image, all of the toolkit tools use one of the these three base docker images:

    - `hyko-sdk-tiny`: used for relatively simple tasks that doesn't require any media input or outputs (video, audio, image...).
    - `hyko-sdk-medium`: used for tools that doesn't use audio type.
    - `hyko-sdk`: used by the rest of the tools.

    > **Note**: You may notice some tools within the `hyko_toolkit` directory lacking a Dockerfile. This is because the toolkit-builder.py script, which we'll cover later, identifies the closest Dockerfile in the parent directory for such tools during its directory traversal process.
