# 4. tjedan — Kontejneri I: Dockerfile

Do sada je aplikacija radila samo na tvom računalu, u tvom `.venv`-u, s tvojom verzijom Pythona. Ovaj tjedan je pakiraš u **Docker image**: jednu datoteku koja sadrži aplikaciju, sve njezine ovisnosti i naredbu za pokretanje. Isti image vrti se na laptopu, u CI-ju (6. tjedan) i u Kubernetesu (10. tjedan).

Na kraju ovog tjedna trebao bi znati:

- objasniti razliku između imagea i kontejnera te što su slojevi (layers),
- napisati `Dockerfile` i složiti ga tako da build koristi cache,
- smanjiti image multi-stage buildom i manjim base imageom,
- pokrenuti aplikaciju kao korisnik koji nije `root`,
- izmjeriti veličinu imagea i znati što broj zapravo znači.

---

## 1. Image, kontejner, sloj

| Pojam | Što je | Analogija |
| --- | --- | --- |
| **image** | zapakiran datotečni sustav + upute za pokretanje, samo za čitanje | klasa |
| **kontejner** | pokrenuti image, s vlastitim procesom i slojem za pisanje | objekt |
| **sloj (layer)** | rezultat jedne naredbe u `Dockerfileu` (`COPY`, `RUN`…) | commit |
| **registry** | mjesto gdje se imagei spremaju i dijele (Docker Hub, GHCR) | GitHub za imagee |

Svaka naredba u `Dockerfileu` napravi novi sloj **povrh prethodnog**. Docker pamti slojeve: ako se naredba i sve prije nje nisu promijenili, sloj se uzme iz cachea i build traje sekundu umjesto minute.

```bash
docker history shortener      # slojevi imagea i koliko je koji velik
```

Važna posljedica: datoteka obrisana u kasnijem sloju **i dalje postoji** u ranijem i image je jednako velik. Zato se smeće ne briše naknadno, nego se uopće ne unosi.

---

## 2. Naivni Dockerfile

Prvi pokušaj, koji radi:

```dockerfile
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t shortener:naive app
docker images shortener
```

Tri problema:

1. **Velik je.** `python:3.12` je cijeli Debian s kompajlerima i alatima za build, pa image za aplikaciju od 130 redova ima **1,3 GB**.
2. **Cache ne pomaže.** `COPY . .` je prije `pip install`, pa svaka promjena u `main.py` poništi cache i ovisnosti se instaliraju ispočetka.
3. **Radi kao `root`.** Provjeri: `docker run --rm --entrypoint whoami shortener:naive`. Ako netko provali u aplikaciju, root je u kontejneru, a jedna greška u konfiguraciji dijeli ga od roota na hostu.

---

## 3. Popravak, korak po korak

Gotov `Dockerfile` je u [`app/Dockerfile`](../app/Dockerfile). Evo zašto izgleda tako.

### 3.1 Manji base image

`python:3.12-slim` je isti Python bez alata za build: oko 150 MB umjesto više od 1 GB. Treba ti kompajler samo ako neki paket nema gotov *wheel*. Naši paketi ga imaju (zato je u `requirements.txt` baš `psycopg[binary]`).

> `alpine` je još manji, ali koristi musl umjesto glibc. Mnogi Python paketi za njega nemaju wheel, pa se kompajliraju i build postane i sporiji i veći. Za Python ostani na `slim`.

### 3.2 Redoslijed zbog cachea

Ono što se rijetko mijenja ide **gore**, a ono što se često mijenja **dolje**:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt   # cache dok se requirements.txt ne promijeni
COPY main.py .                        # mijenja se stalno, zato zadnje
```

Probaj: promijeni poruku u `GET /` i ponovno buildaj. Kod `pip install` mora pisati `CACHED`.

### 3.3 `.dockerignore`

`COPY` šalje Dockeru sve iz mape (*build context*). Bez [`app/.dockerignore`](../app/.dockerignore) u image ulaze testovi, `__pycache__` i, najgore, `.env` s lozinkama. Image se dijeli preko registryja, pa bi lozinku dobio svatko tko ga može povući.

### 3.4 Multi-stage build

Dva `FROM`-a u jednoj datoteci. Prva faza (`builder`) instalira pakete, a druga kopira **samo rezultat**:

```dockerfile
FROM python:3.12-slim AS builder
RUN python -m venv --without-pip /opt/venv
COPY requirements.txt .
RUN pip --python /opt/venv/bin/python install -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
```

Sve što je ostalo u prvoj fazi (pip cache, privremene datoteke, alati za build ako su trebali) **ne ulazi** u finalni image. Ovdje je dobitak mali jer `slim` nema što kompajlirati. Kod paketa koji traže `gcc` razlika je stotine MB, a obrazac je isti.

### 3.5 Non-root korisnik

```dockerfile
RUN useradd --create-home --uid 10001 app
COPY --chown=app:app main.py .
USER app
```

Sve nakon `USER` i sam proces u kontejneru rade kao `app`. Fiksni UID (`10001`) trebat će u 10. tjednu, kad Kubernetes provjerava `runAsNonRoot`.

### 3.6 `HEALTHCHECK`

```dockerfile
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
```

Docker periodički pita tvoj `/health`, a `docker ps` pokaže `healthy` ili `unhealthy`. U `slim` imageu nema `curl`, pa provjeru radi Python. Ovo se isplati u 5. tjednu: Compose čeka da servis postane `healthy` prije nego što pokrene servise koji o njemu ovise.

---

## 4. Usporedba

Izmjereno na oglednoj aplikaciji:

| Image | `docker images` | Stvarni sadržaj | Korisnik |
| --- | --- | --- | --- |
| naivni (`python:3.12`) | 1,78 GB | 1,3 GB | `root` |
| `slim` + multi-stage + non-root | 321 MB | 236 MB | `app` |

**Zašto dva broja?** Docker Desktop (macOS, Windows) s *containerd image storeom* u `docker images` zbraja i komprimirane i raspakirane slojeve, pa je broj veći od onoga što je stvarno u imageu. Čak i prazni `python:3.12-slim` tamo pokazuje 205 MB. Stvarnu veličinu izmjeri ovako:

```bash
docker run --rm --entrypoint du shortener -sxh /
```

Na Linuxu bez containerd storea `docker images` već pokazuje stvarni sadržaj. Za kriterij od 300 MB vrijedi **stvarni sadržaj**. U opis PR-a upiši oba broja i naredbu kojom si mjerio.

Što još zauzima mjesto: `docker run --rm --entrypoint sh shortener -c 'du -sh /opt/venv/lib/python3.12/site-packages/* | sort -h | tail'`.

---

## 5. Pokretanje uz bazu i Redis

U kontejneru `localhost` znači **sam kontejner**, a ne tvoje računalo. Aplikacija zato ne nađe bazu na `localhost:5432`. Do Composea (5. tjedan) rješenje je zajednička Docker mreža, na kojoj se kontejneri nalaze po imenu:

```bash
docker network create shortnet
docker run -d --name pg    --network shortnet --env-file .env postgres:16
docker run -d --name redis --network shortnet redis:7
until docker exec pg pg_isready -h 127.0.0.1 -U app; do sleep 1; done

docker build -t shortener app
docker run -d --name api --network shortnet -p 8000:8000 --env-file .env \
  -e POSTGRES_HOST=pg -e REDIS_URL=redis://redis:6379/0 \
  shortener

curl localhost:8000/health
docker ps                       # nakon ~10 s STATUS: Up … (healthy)
```

`-e` nadjača vrijednosti iz `.env`, pa isti `.env` i dalje radi za `make run`.

Gašenje: `docker rm -f api pg redis && docker network rm shortnet`.

Verziju možeš upisati pri buildu, a `GET /` je pokaže:

```bash
docker build --build-arg APP_VERSION=$(git rev-parse --short HEAD) -t shortener app
```

---

## 6. Optimizacija uz AI

Daj AI alatu svoj naivni `Dockerfile` i traži da ga smanji i učini sigurnijim. Zatim **provjeri** svaki prijedlog:

- buildaj i izmjeri veličinu prije i poslije: je li stvarno manji?
- pokreni kontejner i `curl /health`: radi li i dalje?
- `whoami` u kontejneru: je li stvarno non-root?
- prijedlog s `alpine`: koliko traje build i radi li `psycopg`?

AI često predloži stvari koje zvuče dobro, a ne rade za tvoj slučaj (npr. `pip install --user` pa `USER` bez `PATH`-a, ili `HEALTHCHECK` s `curl`-om kojeg u `slim` nema). Zapiši u [`docs/ai-log.md`](ai-log.md) što je predložio i što si morao ispraviti.

---

## 7. Zadatak `lab-04`

Na grani `lab-04-…`, kao PR s labelom `lab-04`:

**Kriteriji prihvaćanja:**

- [ ] `Dockerfile` za tvoj API (u mapi aplikacije, npr. `app/Dockerfile`)
- [ ] `.dockerignore`: u imageu nema testova, cacheova ni `.env`
- [ ] image je **manji od 300 MB** (stvarni sadržaj, vidi poglavlje 4)
- [ ] aplikacija u kontejneru **ne radi kao `root`**
- [ ] ovisnosti se instaliraju **prije** kopiranja koda (promjena koda ne poništi cache za `pip install`)
- [ ] kontejner se pokreće i `/health` vraća `200` uz bazu i Redis (poglavlje 5)
- [ ] u opisu PR-a: veličina naivnog i optimiziranog imagea i ispis `whoami` iz kontejnera
- [ ] `README.md` (sekcija *Moj projekt*): kako buildati i pokrenuti image
- [ ] ako si koristio AI, zapis u `docs/ai-log.md`

| Bodovi | Kriterij |
| --- | --- |
| 3 | sve iz kriterija prihvaćanja |
| 2 | image radi, ali je veći od 300 MB **ili** radi kao `root` |
| 1 | `Dockerfile` postoji i image se builda, ali kontejner ne radi |
| 0 | nema `Dockerfilea` |

**Rok:** početak sljedećeg termina (računa se otvaranje PR-a).

---

## Česte greške

- **`.env` u imageu.** Provjeri: `docker run --rm --entrypoint ls shortener -la`. Lozinke se predaju pri pokretanju (`--env-file`), nikad pri buildu.
- **`localhost` u kontejneru.** `/health` vraća `503`, a `postgres: fail`. Koristi ime kontejnera i zajedničku mrežu (poglavlje 5).
- **Kontejner odmah izađe.** `docker logs api`. Najčešće je baza još bila u startu (`OperationalError`); pričekaj `pg_isready` i pokreni ponovno.
- **`--host 127.0.0.1` u `CMD`.** Aplikacija tada sluša samo unutar kontejnera i `-p 8000:8000` ne pomaže. Mora biti `0.0.0.0`.
- **`USER` prije `COPY` bez `--chown`.** Datoteke su u vlasništvu roota. Za čitanje to ne smeta, ali aplikacija koja piše u svoju mapu dobije `Permission denied`.
- **Brisanje u zasebnom `RUN`-u** (`RUN rm -rf …`) ne smanjuje image. Datoteka ostaje u ranijem sloju (poglavlje 1).
- **`docker images` pokazuje više od 300 MB** na Docker Desktopu, a stvarno je manje. Izmjeri s `du` (poglavlje 4).
