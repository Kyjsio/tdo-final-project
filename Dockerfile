FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app


ENV PYTHONPATH="${PYTHONPATH}:/app/app"

EXPOSE 6666

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6666"]