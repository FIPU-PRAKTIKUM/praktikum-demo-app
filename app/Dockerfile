# URL shortener — multi-stage, non-root image.
# Build (iz korijena repozitorija):  docker build -t shortener app
# Pokretanje:                        docker run --env-file .env -p 8000:8000 shortener

# --- 1. faza: instalacija ovisnosti u virtualenv -----------------------------
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Venv bez pipa (−13 MB u finalnom imageu); pakete instalira pip iz base imagea.
RUN python -m venv --without-pip /opt/venv

# Prvo samo requirements.txt: dok se ovisnosti ne promijene, ovaj sloj ostaje u cacheu
# i promjena u main.py ne pokreće ponovnu instalaciju.
COPY requirements.txt .
RUN pip --python /opt/venv/bin/python install -r requirements.txt

# --- 2. faza: runtime, bez pip cachea i alata za build ----------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Korisnik bez root ovlasti.
RUN useradd --create-home --uid 10001 app

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY --chown=app:app main.py .

USER app

ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION

EXPOSE 8000

# slim image nema curl, pa provjeru radi Python. /health vraća 503 kad baza ili Redis ne rade.
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
