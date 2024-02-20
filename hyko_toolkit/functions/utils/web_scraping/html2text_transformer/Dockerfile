FROM hyko-sdk:latest
 
RUN pip install --no-cache-dir langchain 
RUN pip install --no-cache-dir html2text
RUN pip install --no-cache-dir BeautifulSoup4
RUN pip install --no-cache-dir bs4

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
