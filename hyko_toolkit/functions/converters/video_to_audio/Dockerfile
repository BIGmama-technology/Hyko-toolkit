FROM hykoai/hyko-sdk-medium:latest

RUN apt-get install -y \
ffmpeg && \
rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
