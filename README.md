# Praktikum — ogledna aplikacija (demo-app)

Ovo je aplikacija koju nastavnik gradi uživo na vježbama. Svaki tjedan dobiva novi sloj infrastrukture — isti koji ti taj tjedan dodaješ na svoju aplikaciju.

Aplikacija je **URL shortener** (API + PostgreSQL + Redis) i zato nije na popisu aplikacija za studente.

## Stanje po tjednima

Nakon svake vježbe stanje repozitorija označeno je git tagom. Ako si izostao ili zapeo, pogledaj točno ono što smo napravili:

```bash
git clone <url-ovog-repozitorija>
cd praktikum-demo-app
git checkout week-02
```

Razliku između dva tjedna vidiš s `git diff week-01 week-02`.

| Tag | Tjedan | Što je dodano | Objašnjenje |
| --- | --- | --- | --- |
| `week-01` | 1 | početno stanje iz predloška (placeholder API) | — |

Tablica se nadopunjuje svaki tjedan.

## Pokretanje

```bash
make run    # API na http://localhost:8000
make test   # testovi
```
