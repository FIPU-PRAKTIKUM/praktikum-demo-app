# app/

Kod aplikacije. Na ovom kolegiju aplikacija je sredstvo, a ne cilj: namjerno je mala, da se možemo baviti onim što je oko nje — kontejnerima, pipelineom, deploymentom i monitoringom.

## Trenutno stanje

Do 3. tjedna ovdje je **placeholder API** iz predloška: jedan FastAPI servis s dva endpointa. U 3. tjednu zamjenjujemo ga URL shortenerom s tri komponente.

| Endpoint | Odgovor | Čemu služi |
| --- | --- | --- |
| `GET /` | `{"message": "...", "version": "dev"}` | provjera da aplikacija radi i koja je verzija deployana |
| `GET /health` | `{"status": "ok", "host": "..."}` | health check za skripte, Docker i Kubernetes |

## Struktura

```
app/
  main.py            # aplikacija
  requirements.txt   # Python ovisnosti s verzijama
  tests/
    test_health.py   # testovi koje pokreće `make test` i CI
```

## `main.py` ukratko

```python
APP_VERSION = os.getenv("APP_VERSION", "dev")
```

Verzija se čita iz **varijable okruženja**, a ne piše u kod. To je prvo od pravila [Twelve-Factor App](https://12factor.net/config): konfiguracija živi u okruženju. Isti image kasnije pokrećemo na stagingu i produkciji samo s drugačijim varijablama. U 7. tjednu CI će u nju upisivati git SHA, pa ćemo na `/` vidjeti točno koji je commit deployan.

```python
@app.get("/health")
def health() -> dict:
    return {"status": "ok", "host": socket.gethostname()}
```

`/health` je ugovor između aplikacije i infrastrukture: "ako odgovorim s 200, spreman sam primati promet". Zasad uvijek vraća `ok`. Kad u 3. tjednu dodamo bazu i Redis, provjeravat će i veze prema njima.

`host` u odgovoru pokazuje ime računala ili kontejnera koji je odgovorio. U 10. tjednu, kad pokrenemo više replika u Kubernetesu, vidjet ćemo kako se zahtjevi raspoređuju po podovima.

## Pokretanje i testovi

```bash
make run     # API na http://localhost:8000, s automatskim reloadom
make test    # testovi
make lint    # provjera stila (ruff)
```

Interaktivna dokumentacija API-ja: http://localhost:8000/docs

## Što slijedi

| Tjedan | Promjena u `app/` |
| --- | --- |
| 3 | URL shortener: API + PostgreSQL + Redis, `/health` provjerava obje veze |
| 4 | `Dockerfile` |
| 12 | `/metrics` endpoint za Prometheus |
