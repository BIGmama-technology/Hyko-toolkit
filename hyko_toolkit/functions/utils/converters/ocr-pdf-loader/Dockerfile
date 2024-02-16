FROM hyko-sdk:latest

WORKDIR /app

COPY . .

RUN poetry run pip install pytesseract pdf2image PyMuPDF
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-fra tesseract-ocr-ara
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
