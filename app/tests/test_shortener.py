import main


def test_shorten_and_redirect(client):
    created = client.post("/shorten", json={"url": "https://example.com/nesto"})
    assert created.status_code == 201
    code = created.json()["code"]
    assert len(code) == main.CODE_LENGTH

    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/nesto"


def test_redirect_fills_cache(client):
    code = client.post("/shorten", json={"url": "https://example.com/"}).json()["code"]
    assert main.cache.get(f"link:{code}") is None
    client.get(f"/{code}", follow_redirects=False)
    assert main.cache.get(f"link:{code}") == "https://example.com/"


def test_redirect_works_without_redis(client, redis_server):
    code = client.post("/shorten", json={"url": "https://example.com/"}).json()["code"]
    redis_server.connected = False
    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 307


def test_unknown_code_is_404(client):
    assert client.get("/nepostoji", follow_redirects=False).status_code == 404


def test_invalid_url_is_rejected(client):
    assert client.post("/shorten", json={"url": "nije-url"}).status_code == 422
