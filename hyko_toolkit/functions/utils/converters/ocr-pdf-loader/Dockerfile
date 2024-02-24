FROM base:latest as deps

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

RUN --mount=type=cache,target=/root/.cache/pip pip install pytesseract 
RUN --mount=type=cache,target=/root/.cache/pip pip install pdf2image 
RUN --mount=type=cache,target=/root/.cache/pip pip install PyMuPDF

FROM hyko-sdk:latest
COPY --from=deps /.venv /.venv

RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-fra tesseract-ocr-ara

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
