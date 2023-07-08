FROM torch-cuda:latest

RUN pip install hyko_sdk==0.1.25
RUN apt update
RUN apt install ffmpeg -y
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
CMD [ "bash" ]