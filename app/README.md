# app/

Kod aplikacije. Na ovom kolegiju aplikacija je sredstvo, a ne cilj: namjerno je mala, da se možemo baviti onim što je oko nje — kontejnerima, pipelineom, deploymentom i monitoringom.

## Što je ovo

**URL shortener** s tri komponente:

```
            POST /shorten              upis
klijent ──────────────────▶  API  ──────────────▶  PostgreSQL   (trajna pohrana)
        ◀──── 307 redirect ──     ◀──── čitanje ──
            GET /{code}           ──── cache ────▶  Redis        (brzi odgovor)
```

| Endpoint | Primjer | Odgovor |
| --- | --- | --- |
| `GET /` | | `{"message": "...", "version": "dev"}` — radi li i koja je verzija deployana |
| `POST /shorten` | `{"url": "https://unipu.hr"}` | `201` i `{"code": "aB3xZ9", "url": "..."}` |
| `GET /{code}` | `/aB3xZ9` | `307` redirect na spremljeni URL, ili `404` |
| `GET /health` | | `200` ako rade i baza i Redis, inače `503` — s popisom što ne radi |

## Struktura

```
app/
  main.py                # cijela aplikacija (~130 redova)
  requirements.txt       # ovisnosti aplikacije (idu u Docker image)
  requirements-dev.txt   # + pytest, ruff i fakeredis (ne idu u image)
  tests/
    conftest.py          # zamjena PostgreSQL → SQLite i Redis → fakeredis
    test_health.py       # /health: 200 kad sve radi, 503 kad Redis padne
    test_shortener.py    # skraćivanje, redirect, cache, 404, neispravan URL
```

## `main.py` ukratko

### Konfiguracija iz okruženja

```python
DATABASE_URL = URL.create(
    "postgresql+psycopg",
    username=os.getenv("POSTGRES_USER", "app"),
    password=os.getenv("POSTGRES_PASSWORD", ""),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    ...
    query={"connect_timeout": "2"},
)
```

Ništa nije upisano u kod: korisnik, lozinka i adresa baze dolaze iz **varijabli okruženja** ([Twelve-Factor App](https://12factor.net/config)). Iste varijable (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) čita i službeni postgres image, pa jedan `.env` konfigurira i bazu i aplikaciju. Lozinka nema zadanu vrijednost — ne želimo je u gitu (u 13. tjednu gitleaks bi je našao).

`connect_timeout=2`: bez toga bi `/health` visio desetke sekundi kad baza ne odgovara, umjesto da brzo javi `503`.

### `/health` — ugovor s infrastrukturom

```python
@app.get("/health")
def health(response: Response) -> dict:
    ...  # SELECT 1 na bazu, PING na Redis
    if not healthy:
        response.status_code = 503
```

`/health` odgovara na pitanje "jesam li spreman primati promet?". Proces koji radi, a ne može do baze, **nije** spreman. Zato `503`, a ne `200` s porukom o grešci: skripte, Docker i Kubernetes gledaju **status kod**, ne tekst. Skripta iz 2. tjedna (`curl -f`) to odmah prijavi kao `FAIL`.

`host` u odgovoru pokazuje koji je kontejner odgovorio — u 10. tjednu tako vidimo raspodjelu prometa po podovima.

### Redirect: prvo cache, onda baza

```python
try:
    url = cache.get(key)
except redis.RedisError:
    url = None          # Redis ne radi → nastavi bez njega
if url is None:
    url = ... iz PostgreSQL-a ...
    cache.set(key, url, ex=CACHE_TTL)
```

Klasični **cache-aside** obrazac. Redis je ubrzanje, ne izvor istine: ako padne, redirect i dalje radi (sporije), a `/health` javlja `503` da netko to popravi.

### Tablica pri pokretanju

`lifespan` pri startu napravi tablicu `links` ako ne postoji. Ako baza tada ne radi, aplikacija **ne krene** — namjerno. U 5. tjednu `depends_on` u Composeu, a u 10. tjednu Kubernetes, pobrinut će se da se pokreće redom i ponovno.

## Pokretanje

Treba ti PostgreSQL i Redis. Do 5. tjedna (Compose) dižemo ih ručno:

```bash
cp .env.example .env                      # jednom; po želji promijeni lozinku
docker run -d --name pg --env-file .env -p 5432:5432 postgres:16
docker run -d --name redis -p 6379:6379 redis:7

make install                # jednom: .venv i ovisnosti
source .venv/bin/activate   # u svakom novom terminalu
make run                    # API na http://localhost:8000, čita .env
```

Probaj:

```bash
curl localhost:8000/health
curl -X POST localhost:8000/shorten -H 'Content-Type: application/json' -d '{"url":"https://unipu.hr"}'
curl -i localhost:8000/<code>            # 307 i Location
docker stop redis && curl -i localhost:8000/health   # 503
docker start redis
```

Interaktivna dokumentacija: http://localhost:8000/docs

Gašenje: `docker rm -f pg redis` (podaci u bazi se brišu — trajni volumeni dolaze u 5. tjednu).

## Testovi

```bash
make test    # 8 testova, bez prave baze i Redisa
make lint
```

Testovi u `conftest.py` podmetnu SQLite bazu u memoriji umjesto PostgreSQL-a i `fakeredis` umjesto Redisa. Zato `make test` i CI rade bez ikakvih servisa. `test_health_503_when_redis_is_down` "ugasi" lažni Redis i provjeri da `/health` vrati `503`.

## Što slijedi

| Tjedan | Promjena u `app/` |
| --- | --- |
| 4 | `Dockerfile` |
| 5 | API, PostgreSQL i Redis zajedno u `compose.yaml` |
| 12 | `/metrics` endpoint za Prometheus |
