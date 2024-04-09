<!-- x-release-please-start-version -->
 ![Static Badge](https://img.shields.io/badge/Release-v2.1.0-/?style=flat&logo=track)
<!-- x-release-please-end -->

# Hyko toolkit

## Table of contents
- [Description](#description)
- [Toolkit components](#toolkit-components)
    - [Functions and Models](#functions-and-models)
    - [APIs](#apis)
- [Adding new function/model to the toolkit](#adding-new-functionmodel-to-the-toolkit)
- [Adding new api to the toolkit](#adding-new-api-to-the-toolkit)
- [The toolkit_builder script](#the-toolkit_builderpy-script)
- [Building the toolkit](#building-the-toolkit)

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

- **Add a Dockerfile for your function/model**:

    `Dockerfile`: After finishing up with `metadata.py` and `main.py` file, the fastapi app needs to be packaged inside a docker image, all of the toolkit tools use one of the these three base docker images:

    - `hyko-sdk-tiny`: used for relatively simple tasks that doesn't require any media input or outputs (video, audio, image...).
    - `hyko-sdk-medium`: used for tools that doesn't use audio type.
    - `hyko-sdk`: used by the rest of the tools.

    > **Note**: You may notice some tools within the `hyko_toolkit` directory lacking a Dockerfile. This is because the toolkit-builder.py script, which we'll cover later, identifies the closest Dockerfile in the parent directory for such tools during its directory traversal process.


## Adding new api to the toolkit

Adding an API to the Hyko Toolkit is a streamlined process compared to functions and models, requiring only one file: the `metadata.py` file. In this file, we follow a similar approach as with functions and models, documenting essential metadata such as inputs, parameters, outputs, name, description, and task. However, for APIs, we include an additional step: making the call to the API using httpx while adhering to the API specification.

Here's a breakdown of the steps involved:

1. **Create metadata.py File**:

    - Develop a metadata.py file within the designated category directory (e.g., apis).
    - Document key metadata for the API, including inputs, parameters, outputs, name, description, and task.

2. **API Call Implementation**:

    - Incorporate the API call within the metadata.py file, utilizing httpx.
    - Ensure that the API call conforms to the specifications outlined by the respective API.

3. **Import your API in `__init__.py`**

    - By importing the API in the `__init__.py` it will be registered and discoverable by the backend.  


## The `toolkit_builder.py` script

The toolkit_builder script, written in Python, serves as a crucial tool for the Hyko Toolkit, facilitating two primary functions:

1. **Docker Image Building**: For functions and models found within the `hyko_toolkit` directory, the script first builds the Docker image specific to each tool.

2. **Metadata Extraction and Database Writing**: Subsequently, the script traverses through all categories (functions, models, and APIs), extracting metadata for each tool. This includes JSON schema information for inputs, parameters, and outputs defined in the metadata.py file. The extracted metadata is then written to the Hyko database, utilizing credentials specified in the `.env` file.

## Building the toolkit

Follow these steps to set up and build the Hyko Toolkit:

1. Ensure you have Poetry and pyenv installed on your system. You can refer to the following links for installation guidance:

- [Poetry](https://python-poetry.org/docs/#installation)
- [Pyenv](https://github.com/pyenv/pyenv)

2. Clone the repository:

    ```bash
    git clone https://github.com/BIGmama-technology/Hyko-toolkit.git toolkit
    ```

    ```bash
    cd toolkit
    ```

3. Execute the setup script to install the Python version used with the Hyko Toolkit (3.11.6) and install the required dependencies using Poetry. This script also activates the new virtual environment.

    ```bash
    make setup
    ```

4. Copy the `.env.example` file and rename it to `.env`.

    ```bash
    cp .env.example .env
    ```

5. Build the toolkit: Use the build command to execute the `toolkit_builder.py` script. You can specify optional parameters:

    **`dir`** (default: hyko_toolkit): the directory you want the `toolkit_builder.py` script to go through (Make sure to only specify directories that have `Dockerfile` in them since the script right now can't go backwards when traversing the tree, only down.)

    **`host`** (default: traefik.me): this is used to specify which running backend to write to it the toolkit metadata (At this point you should have your credentials in the `.env` file else the api will return a 401 response).

    ```bash
    make build dir=hyko_toolkit/functions/utils host=stage.hyko.ai
    ```
