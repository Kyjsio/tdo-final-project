FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim AS runtime

WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app/app"

EXPOSE 6666

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6666"]