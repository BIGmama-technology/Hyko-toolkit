FROM hyko-sdk:latest

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

RUN --mount=type=cache,target=/root/.cache/pip pip install pygments 
RUN --mount=type=cache,target=/root/.cache/pip pip install fpdf2 
RUN --mount=type=cache,target=/root/.cache/pip pip install markdown
COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
