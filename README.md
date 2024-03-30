<!-- x-release-please-start-version -->
 ![Static Badge](https://img.shields.io/badge/Release-v2.0.0-/?style=flat&logo=track)
<!-- x-release-please-end -->

# Hyko toolkit

## Table of contents
- [Description](#description)
- [Toolkit components](#toolkit-components)
    - [Functions and Models](#functions-and-models)
    - [APIs](#apis)

## Description

[Hyko](https://hyko.ai) Toolkit stands as a robust repository housing a diverse collection of tools. From a curated selection of functions and APIs to state-of-the-art AI models, each component has been meticulously crafted to empower developers in constructing versatile blueprints effortlessly.


## Toolkit components.

The Hyko Toolkit consists of three primary categories of components: **_functions_**, **_models_**, and **_APIs_**. Let's delve into functions and models first, as they share many similarities.

- <span id="functions-and-models">**_Functions_** and **_Models_**</span>: These are essentially FastAPI applications that define a specific set of inputs, parameters, and outputs. This metadata is crucial for both the Hyko frontend and backend to effectively utilize these functions and models. After defining the metadata, the FastAPI application is packaged and bundled into a Docker image. When executing a task involving a particular function or model, this Docker image is built on the local machine.

- <span id="apis">**_APIs_**</span>: Similar to functions and models, APIs also require inputs, parameters, and outputs to extract metadata. However, APIs differ in that they do not necessitate local execution on a computer. Therefore, there's no need for a Docker image or a FastAPI application. Instead, the Hyko backend makes requests to these external APIs. These APIs can range from OpenAI and Hugging Face inference APIs to OpenRouter APIs, and beyond.
