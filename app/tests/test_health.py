def test_root_has_version(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_health_ok_when_dependencies_work(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["checks"] == {"postgres": "ok", "redis": "ok"}


def test_health_503_when_redis_is_down(client, redis_server):
    redis_server.connected = False
    response = client.get("/health")
    assert response.status_code == 503
    assert response.json()["status"] == "fail"
    assert response.json()["checks"]["redis"] == "fail"
