FROM python:3.11-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY ws_client.py .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ws_client.py"]
