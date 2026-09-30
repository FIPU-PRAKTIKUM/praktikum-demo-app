"""Placeholder API.

Ovo je minimalna aplikacija da pipeline od prvog dana ima što buildati i testirati.
Zamijeni je svojom aplikacijom (ili je proširi) do 3. tjedna.
"""

import os
import socket

from fastapi import FastAPI

app = FastAPI(title="praktikum-api")

APP_VERSION = os.getenv("APP_VERSION", "dev")


@app.get("/")
def root() -> dict:
    return {"message": "Pozdrav iz praktikuma!", "version": APP_VERSION}


@app.get("/health")
def health() -> dict:
    """Liveness/readiness probe za Docker i Kubernetes."""
    return {"status": "ok", "host": socket.gethostname()}
