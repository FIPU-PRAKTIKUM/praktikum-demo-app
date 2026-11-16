"""URL shortener — ogledna aplikacija s vježbi.

Tri komponente: ovaj API, PostgreSQL (trajna pohrana linkova) i Redis (cache).
Sva konfiguracija dolazi iz varijabli okruženja (vidi .env.example).
"""

import os
import secrets
import socket
import string
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy import Column, MetaData, String, Table, Text, create_engine, insert, select, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

APP_VERSION = os.getenv("APP_VERSION", "dev")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # koliko sekundi link ostaje u Redisu
CODE_LENGTH = 6
ALPHABET = string.ascii_letters + string.digits

# --- PostgreSQL -------------------------------------------------------------
# Iste varijable čita i sam postgres kontejner, pa obje strane koriste isti .env.
DATABASE_URL = URL.create(
    "postgresql+psycopg",
    username=os.getenv("POSTGRES_USER", "app"),
    password=os.getenv("POSTGRES_PASSWORD", ""),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    database=os.getenv("POSTGRES_DB", "app"),
    query={"connect_timeout": "2"},  # bez ovoga /health visi kad baza ne odgovara
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

metadata = MetaData()
links = Table(
    "links",
    metadata,
    Column("code", String(CODE_LENGTH), primary_key=True),
    Column("url", Text, nullable=False),
)

# --- Redis ------------------------------------------------------------------
cache = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    socket_timeout=1,
    socket_connect_timeout=1,
    decode_responses=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pri pokretanju napravi tablicu ako ne postoji. Ako baza ne radi, aplikacija se
    # neće pokrenuti — bolje glasno pasti nego tiho raditi pola posla.
    metadata.create_all(engine)
    yield


app = FastAPI(title="praktikum-shortener", lifespan=lifespan)


class ShortenRequest(BaseModel):
    url: HttpUrl


def new_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


@app.get("/")
def root() -> dict:
    return {"message": "Pozdrav iz praktikuma!", "version": APP_VERSION}


@app.get("/health")
def health(response: Response) -> dict:
    """Spreman sam samo ako rade i baza i cache. Inače 503."""
    checks = {}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except SQLAlchemyError:
        checks["postgres"] = "fail"
    try:
        cache.ping()
        checks["redis"] = "ok"
    except redis.RedisError:
        checks["redis"] = "fail"

    healthy = all(v == "ok" for v in checks.values())
    if not healthy:
        response.status_code = 503
    return {"status": "ok" if healthy else "fail", "host": socket.gethostname(), "checks": checks}


@app.post("/shorten", status_code=201)
def shorten(req: ShortenRequest) -> dict:
    url = str(req.url)
    for _ in range(5):  # kod je nasumičan; ako je slučajno zauzet, probaj drugi
        code = new_code()
        try:
            with engine.begin() as conn:
                conn.execute(insert(links).values(code=code, url=url))
            return {"code": code, "url": url}
        except IntegrityError:
            continue
    raise HTTPException(status_code=500, detail="Ne mogu generirati jedinstveni kod")


@app.get("/{code}")
def redirect(code: str) -> RedirectResponse:
    key = f"link:{code}"

    # 1. Cache. Ako Redis ne radi, ne rušimo se — idemo ravno u bazu.
    try:
        url = cache.get(key)
    except redis.RedisError:
        url = None

    # 2. Baza.
    if url is None:
        with engine.connect() as conn:
            url = conn.execute(select(links.c.url).where(links.c.code == code)).scalar()
        if url is None:
            raise HTTPException(status_code=404, detail="Nepoznat kod")
        try:
            cache.set(key, url, ex=CACHE_TTL)
        except redis.RedisError:
            pass

    return RedirectResponse(url, status_code=307)
