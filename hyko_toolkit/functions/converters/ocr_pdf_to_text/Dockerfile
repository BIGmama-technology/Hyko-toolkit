FROM hyko-sdk-medium:latest

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

RUN apt-get update && apt-get install -y\
tesseract-ocr\
libtesseract-dev\
tesseract-ocr-fra\
tesseract-ocr-ara &&\
rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/pip pip install pytesseract 
RUN --mount=type=cache,target=/root/.cache/pip pip install pdf2image 
RUN --mount=type=cache,target=/root/.cache/pip pip install PyMuPDF

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
