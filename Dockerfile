FROM python:3.10-slim

WORKDIR /app

# 1. Instalacja bibliotek
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Zachowujemy strukturę folderów (app wewnątrz app)
COPY app/ ./app

# 3. MAGICZNA NAPRAWA IMPORTÓW:
# Mówimy Pythonowi: "Szukaj modułów w /app ORAZ w /app/app"
# Dzięki temu main.py znajdzie "routers", a routers znajdzie "app"
ENV PYTHONPATH="${PYTHONPATH}:/app/app"

EXPOSE 6666

# 4. Uruchamiamy
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6666"]