"""Testovi rade bez prave baze i Redisa.

PostgreSQL zamjenjujemo SQLite bazom u memoriji, a Redis s fakeredis.
Tako `make test` i CI ne trebaju nikakve servise.
"""

import fakeredis
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

import main


@pytest.fixture
def redis_server():
    return fakeredis.FakeServer()


@pytest.fixture
def client(monkeypatch, redis_server):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # sve konekcije dijele istu bazu u memoriji
    )
    monkeypatch.setattr(main, "engine", engine)
    fake_cache = fakeredis.FakeRedis(server=redis_server, decode_responses=True)
    monkeypatch.setattr(main, "cache", fake_cache)
    with TestClient(main.app) as c:  # "with" pokreće lifespan, tj. create_all
        yield c
