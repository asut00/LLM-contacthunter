FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt update && apt install -y net-tools
RUN apt install curl -y
RUN apt install vim -y

RUN apt-get update && apt-get install -y \
    poppler-utils \
	tesseract-ocr

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
