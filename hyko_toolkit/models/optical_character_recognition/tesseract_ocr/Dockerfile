FROM hyko-sdk-medium:latest

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

RUN --mount=type=cache,target=/root/.cache/pip pip install pytesseract 
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-fra tesseract-ocr-ara tesseract-ocr-spa

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
