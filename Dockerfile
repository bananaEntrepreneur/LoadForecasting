FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .


FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python*/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

EXPOSE 8000
EXPOSE 8501

CMD ["sh", "-c", "python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 & python -m streamlit run src/app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true"]