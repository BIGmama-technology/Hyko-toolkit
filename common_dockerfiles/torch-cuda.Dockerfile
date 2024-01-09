FROM hyko-sdk:latest

RUN poetry add transformers[torch] diffusers[torch] accelerate sentencepiece
