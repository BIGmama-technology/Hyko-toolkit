FROM hyko-sdk:latest

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

RUN pip install --no-cache-dir pytesseract 
RUN pip install --no-cache-dir pdf2image 
RUN pip install --no-cache-dir PyMuPDF
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-fra tesseract-ocr-ara

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
