# 5. tjedan — Kontejneri II: Docker Compose

Prošli tjedan API je dobio svoj image, ali za pokretanje cijelog stacka trebalo je pet `docker run` naredbi, ručno napravljena mreža i čekanje da se baza digne. Ovaj tjedan sve to opisuješ u **jednoj datoteci**, `compose.yaml`, a cijeli stack diže i gasi **jedna naredba**. Isti opis servisa, mreže i volumena vratit će se u Kubernetesu (10. tjedan), samo drugim alatom.

Na kraju ovog tjedna trebao bi znati:

- opisati multi-service aplikaciju u `compose.yaml`: servise, mrežu i volumene,
- objasniti zašto se servisi u Composeu nalaze po imenu, a ne na `localhost`,
- složiti redoslijed pokretanja tako da API čeka da baza bude **spremna**, a ne samo pokrenuta,
- sačuvati podatke baze kroz `docker compose down` i `up`,
- držati lozinke u `.env`, izvan gita i izvan `compose.yaml`.

---

## 1. Od pet naredbi do jedne datoteke

Ovako smo stack dizali u 4. tjednu:

```bash
docker network create shortnet
docker run -d --name pg    --network shortnet --env-file .env postgres:16
docker run -d --name redis --network shortnet redis:7
until docker exec pg pg_isready -h 127.0.0.1 -U app; do sleep 1; done
docker run -d --name api --network shortnet -p 8000:8000 --env-file .env \
  -e POSTGRES_HOST=pg -e REDIS_URL=redis://redis:6379/0 shortener
```

Sve to je znanje koje živi u tvojoj glavi ili u povijesti terminala. Kolega koji klonira repo ne zna ni redoslijed ni zastavice. Compose to isto znanje zapiše **deklarativno**: opišeš *što* treba postojati, a Compose sam napravi mrežu, pokrene kontejnere ispravnim redom i pospremi za sobom.

| Pojam | Što je | U `docker run` svijetu |
| --- | --- | --- |
| **servis** | jedan kontejner (ili više kopija) s imageom i konfiguracijom | jedna `docker run` naredba |
| **projekt** | svi servisi iz jednog `compose.yaml`; ime je ime mape | — |
| **mreža** | Compose za projekt sam napravi mrežu `<projekt>_default` | `docker network create` |
| **volumen** | trajni podaci izvan kontejnera, preživljavaju brisanje kontejnera | `-v ime:/putanja` |

> Datoteka se zove `compose.yaml`. Stariji `docker-compose.yml` i dalje radi, kao i naredba `docker-compose` s crticom (v1), ali v1 se više ne razvija. Na kolegiju koristimo `docker compose` (v2, plugin Dockera).

---

## 2. `compose.yaml` korak po korak

Gotova datoteka je u [`compose.yaml`](../compose.yaml) u korijenu repozitorija. Slaže se ovim redom.

### 2.1 Baza i cache

```yaml
services:
  db:
    image: postgres:16
    env_file: .env

  cache:
    image: redis:7
```

`postgres:16` čita `POSTGRES_USER`, `POSTGRES_PASSWORD` i `POSTGRES_DB` iz okruženja i pri prvom pokretanju napravi korisnika i bazu. To su iste varijable koje čita i naš API, pa obje strane dijele isti `.env`.

Primijeti da `db` i `cache` **nemaju `ports`**. Baza ne treba biti dostupna s tvog računala, nego samo API-ju, a API je u istoj mreži.

### 2.2 API iz vlastitog Dockerfilea

```yaml
  api:
    build:
      context: ./app
    image: shortener
    env_file: .env
    environment:
      POSTGRES_HOST: db
      REDIS_URL: redis://cache:6379/0
    ports:
      - "8000:8000"
```

- **`build: context: ./app`** — Compose builda image iz `app/Dockerfile` iz 4. tjedna. `image: shortener` samo daje ime rezultatu.
- **`environment` nadjačava `env_file`.** U `.env` piše `POSTGRES_HOST=localhost`, jer to treba za `make run`. U Composeu baza nije na `localhost`, nego na hostu **`db`**: to je ime servisa. Compose u mreži projekta vrti DNS u kojem je svaki servis dostupan po svom imenu.
- **`ports: "8000:8000"`** — samo API je otvoren prema računalu. Format je isti kao `-p`: `računalo:kontejner`.

```bash
docker compose exec api python -c "import socket; print(socket.gethostbyname('db'))"   # IP baze u mreži
```

### 2.3 Pokrenut ≠ spreman: `healthcheck` i `depends_on`

```yaml
  api:
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy

  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -h 127.0.0.1 -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 3s
      retries: 10
```

Obični `depends_on: [db]` čeka samo da se kontejner baze **pokrene**. Postgres nakon toga treba još nekoliko sekundi, a pri prvom pokretanju i više, jer tada pravi bazu. Naš API pri startu radi `metadata.create_all(engine)` i, ako baza još ne prima veze, odmah padne s `OperationalError`. Na brzom računalu s već skinutim imageima utrka se često ne vidi, pa se lako zaključi da sve radi. Na sporijem laptopu ili u CI-ju puca.

`condition: service_healthy` znači: pokreni API tek kad healthcheck baze javi da je **zdrava**.

- **`pg_isready -h 127.0.0.1`** — dok postgres prvi put inicijalizira bazu, privremeno sluša samo na Unix socketu. Bez `-h` provjera bi prošla prerano.
- **`$${POSTGRES_USER}`** — dvostruki `$` znači da varijablu ne zamjenjuje Compose pri čitanju datoteke, nego shell **u kontejneru**, gdje ona postoji.
- API nema `healthcheck` u `compose.yaml` jer ga već ima u `Dockerfileu` (`HEALTHCHECK`, 4. tjedan). Compose ga koristi, pa `docker compose ps` za API pokazuje `(healthy)`.

**`restart: unless-stopped`** — ako proces u kontejneru padne, Docker ga ponovno pokrene. To ne zamjenjuje `depends_on`: bez njega API svejedno pada dok baza ne dođe, samo se vrti u krug.

### 2.4 Volumen za bazu

```yaml
  db:
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Podaci zapisani u kontejner žive u njegovom sloju za pisanje (4. tjedan, poglavlje 1) i nestaju s njim. Image `postgres` to pokušava spriječiti: u svom Dockerfileu ima `VOLUME /var/lib/postgresql/data`, pa Docker za bazu sam napravi **anonimni** volumen s nasumičnim imenom (`docker volume ls`). Nakon `docker compose down` novi kontejner baze dobije **novi** anonimni volumen i ne nađe stari. Kratki linkovi su „nestali”, a stari volumen ostaje na disku kao smeće.

**Named volume** (`pgdata`) je spremište kojim upravlja Docker, izvan kontejnera. Novi kontejner baze dobije isti volumen i nađe stare podatke.

| Naredba | Kontejneri | Mreža | Volumeni (podaci) |
| --- | --- | --- | --- |
| `docker compose stop` | zaustavljeni, ostaju | ostaje | ostaju |
| `docker compose down` | obrisani | obrisana | **ostaju** |
| `docker compose down -v` | obrisani | obrisana | **obrisani** |

> `down -v` je jedini način da se baza vrati na prazno, ali i najlakši način da izgubiš podatke. U produkciji se za to nikad ne koristi Compose naredba, nego backup.

*Bind mount* (`./podaci:/var/lib/postgresql/data`) mapira mapu s tvog računala. Za kod u razvoju zna biti zgodan, ali za bazu donosi probleme s dozvolama (posebno na Windowsima i WSL-u), pa za podatke koristi named volume.

---

## 3. Konfiguracija i tajne: `.env`

`.env` u Composeu ima **dvije uloge**, i dobro ih je razlikovati:

1. **Interpolacija u `compose.yaml`.** Compose sam čita `.env` iz mape projekta i zamjenjuje `${VARIJABLA}` u datoteci. Tako `APP_VERSION: ${APP_VERSION:-dev}` dobije vrijednost iz `.env`, a ako je nema, `dev`.
2. **Okruženje kontejnera.** `env_file: .env` predaje sve varijable iz datoteke procesu u kontejneru. Bez toga kontejner ne vidi ništa od onoga što je u `.env`.

| Datoteka | U gitu? | Što je u njoj |
| --- | --- | --- |
| `.env.example` | **da** | koje varijable postoje, s lažnim vrijednostima |
| `.env` | **ne** (`.gitignore`) | stvarne vrijednosti na tvom računalu |

```bash
cp .env.example .env          # jednom, nakon kloniranja
git check-ignore -v .env      # mora ispisati pravilo iz .gitignore
docker compose config         # konačna konfiguracija, s varijablama već zamijenjenima
```

> `docker compose config` ispisuje i **lozinke**. Ne lijepi njegov izlaz u PR, forum ni AI chat.

Lozinka upisana izravno u `compose.yaml` (`POSTGRES_PASSWORD: tajna`) završi u gitu, a git **pamti zauvijek**: brisanje u sljedećem commitu ne pomaže (vidi [šalabahter, poglavlje 12](git-cheatsheet.md#12-kad-nešto-pođe-po-zlu)).

---

## 4. Health check skripta vidi cijeli stack

U 2. tjednu skripta [`scripts/healthcheck.sh`](../scripts/healthcheck.sh) dobila je komentar *„5. tjedan: ovdje dodajemo ostale servise”*. Baza i Redis ne govore HTTP, pa za njih `curl` ne pomaže. Skripta se zato malo generalizira: ako je provjera URL, radi je `curl` kao i prije, a sve ostalo je naredba čiji se exit code gleda.

```bash
SERVICES=(
  "api=http://localhost:8000/health"
  "db=docker compose exec -T db pg_isready -h 127.0.0.1 -q"
  "cache=docker compose exec -T cache redis-cli ping"
)
```

- **`docker compose exec -T`** pokreće naredbu u kontejneru koji već radi. `-T` isključuje terminal, što treba kad naredbu ne pokreće čovjek (cron).
- **`cd "$(dirname "$0")/.."`** — `docker compose` traži `compose.yaml` u trenutnoj mapi, a cron kreće iz `$HOME` (2. tjedan, poglavlje 3). Skripta se zato prvo premjesti u korijen repozitorija.

Novi servis i dalje znači **jedan novi red**. Logika je dobila samo jedan `if`. Objašnjenje linija po liniju je u [`scripts/README.md`](../scripts/README.md).

```bash
docker compose stop cache
./scripts/healthcheck.sh; echo "exit: $?"   # api FAIL (503), cache FAIL → exit 1
docker compose start cache
```

API pada zajedno s Redisom jer njegov `/health` provjerava obje ovisnosti (3. tjedan). To je željeno ponašanje: servis koji ne može raditi ne smije javljati da je zdrav.

---

## 5. Naredbe

| Naredba | Što radi |
| --- | --- |
| `docker compose up -d --build` | builda image ako treba i diže sve u pozadini |
| `docker compose up -d --wait` | isto, ali čeka da svi servisi budu `healthy` |
| `docker compose ps` | stanje servisa (`healthy`, `starting`, `unhealthy`) |
| `docker compose logs -f api` | log jednog servisa, uživo |
| `docker compose exec db psql -U app` | ulaz u bazu |
| `docker compose exec cache redis-cli keys 'link:*'` | što je u cacheu |
| `docker compose restart api` | ponovno pokreni jedan servis |
| `docker compose down` | ugasi i obriši kontejnere i mrežu; **podaci ostaju** |
| `docker compose down -v` | isto, ali briše i volumene, tj. **bazu** |
| `docker compose config` | provjeri i ispiši konačnu konfiguraciju |

Probaj cijeli krug:

```bash
docker compose up -d --build --wait
curl -s -X POST localhost:8000/shorten -H 'content-type: application/json' -d '{"url":"https://fipu.unipu.hr"}'
curl -i localhost:8000/<code>                  # 307 → fipu.unipu.hr
docker compose down && docker compose up -d --wait
curl -i localhost:8000/<code>                  # i dalje 307: link je u volumenu
```

### Trebam i `make run`?

`make run` pokreće API izvan Dockera i traži bazu na `localhost:5432`. Ako tako želiš razvijati, digni samo ovisnosti i privremeno im otvori portove samo prema svom računalu:

```yaml
  db:
    ports:
      - "127.0.0.1:5432:5432"   # samo localhost, ne cijela mreža
```

```bash
docker compose up -d db cache
make run
```

---

## 6. Zadatak `lab-05`

Na grani `lab-05-…`, kao PR s labelom `lab-05`:

**Kriteriji prihvaćanja:**

- [ ] `compose.yaml` u korijenu repozitorija sa **svim** komponentama tvoje aplikacije (API, baza, cache…)
- [ ] API se builda iz tvog `Dockerfilea` iz 4. tjedna (`build:`)
- [ ] `cp .env.example .env && docker compose up -d --build` digne cijeli stack **bez ručnih koraka**
- [ ] `healthcheck` na bazi i cacheu, `depends_on` s `condition: service_healthy`
- [ ] named volume za bazu: podaci preživljavaju `docker compose down` i `up`
- [ ] lozinke samo u `.env` (u `.gitignore`); u gitu je `.env.example`
- [ ] samo API ima `ports`
- [ ] `scripts/healthcheck.sh` (iz 2. tjedna) provjerava i nove servise
- [ ] u opisu PR-a: ispis `docker compose ps` (svi `healthy`) i dokaz da link (ili tvoj zapis) preživi `down`/`up`
- [ ] `README.md` (sekcija *Moj projekt*): kako dići stack
- [ ] ako si koristio AI, zapis u `docs/ai-log.md`

| Bodovi | Kriterij |
| --- | --- |
| 3 | sve se diže bez ručnih koraka, healthcheckovi, volumen za bazu, lozinke u `.env` |
| 2 | diže se, ali nema healthcheckova **ili** je lozinka u `compose.yaml` |
| 1 | diže se tek uz ručne korake (npr. ponovno pokretanje API-ja) |
| 0 | stack se ne diže |

**Rok:** početak sljedećeg termina (računa se otvaranje PR-a).

Brza samoprovjera prije PR-a:

```bash
docker compose down -v                 # kreni od nule, kao nastavnik
docker compose up -d --build --wait    # mora završiti bez greške
docker compose ps                      # svi (healthy)
git ls-files | grep -E '^\.env$'       # mora biti prazno
```

---

## Česte greške

- **`POSTGRES_HOST=localhost` u kontejneru.** `/health` vraća `postgres: fail`. U Composeu je baza na hostu koji se zove kao servis (`db`). Postavi to u `environment:` servisa, a `.env` ostavi za `make run`.
- **API pada pri prvom pokretanju, drugi put radi.** To je utrka s bazom. Fali `condition: service_healthy` ili healthcheck baze prolazi prerano (`pg_isready` bez `-h 127.0.0.1`).
- **`env file .env not found`.** Nisi napravio `.env`: `cp .env.example .env`.
- **Lozinka promijenjena u `.env`, a baza je i dalje ne prima.** Postgres čita `POSTGRES_PASSWORD` **samo pri prvom pokretanju**, kad je volumen prazan. Nakon toga lozinka je zapisana u bazi. Za lokalni razvoj: `docker compose down -v` (briše podatke!).
- **`port is already allocated`.** Na računalu već radi nešto na tom portu, najčešće kontejneri iz 4. tjedna (`docker rm -f api pg redis`) ili lokalni postgres. `docker ps` i `lsof -i :8000`.
- **Promjena koda se ne vidi.** `docker compose up -d` ne builda ponovno image koji već postoji. Koristi `--build`.
- **`ports` na bazi i Redisu „za svaki slučaj”.** Redis bez lozinke otvoren na `0.0.0.0:6379` dostupan je svima u istoj mreži (laboratorij, kafić). Otvaraj samo ono što treba, i onda samo na `127.0.0.1`.
- **Na 8 GB RAM-a sve je sporo.** Docker Desktop + tri kontejnera + IDE + preglednik je puno. Zatvori što ne trebaš; u WSL-u provjeri `memory=` u `.wslconfig` (1. tjedan).
