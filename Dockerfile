FROM python:3.10 AS main

ARG CATEGORY
ARG FUNCTION_NAME

COPY ./sdk/common /sdk/common
COPY ./sdk/${CATEGORY}/${FUNCTION_NAME} /sdk/function
RUN pip install -r /sdk/function/requirements.txt

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "sdk.function.main:app"]

FROM main AS metadata

CMD ["python", "-m", "sdk.function.config"]