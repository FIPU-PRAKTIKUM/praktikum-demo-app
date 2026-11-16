# 6. tjedan — Continuous Integration

Do sada je „radi” značilo „radi na mom računalu”. Ovaj tjedan to postaje „radi na čistom računalu koje nije moje, na svaku promjenu”. **CI pipeline** na svaki pull request sam provjeri kod, pokrene testove i builda Docker image. Ako bilo što ne prođe, PR je crven i merge je blokiran. Isti pipeline u 7. tjednu image i objavljuje, a u 13. ga skenira.

Na kraju ovog tjedna trebao bi znati:

- objasniti što je CI i zašto se pokreće na svaki PR, a ne „kad se sjetim”,
- pročitati GitHub Actions workflow: `on`, `jobs`, `steps`, `uses` i `run`,
- dodati job koji builda image i složiti redoslijed jobova s `needs`,
- ubrzati pipeline cacheom (pip i Docker slojevi),
- pročitati log crvenog pipelinea i popraviti uzrok,
- označiti jobove kao *required checks* u branch protectionu.

---

## 1. Što je CI

**Continuous Integration** je praksa da se svaka promjena **često** spaja u glavnu granu i da se pri tome **automatski** provjeri. Male promjene koje se provjeravaju odmah lakše je popraviti nego veliku hrpu na kraju tjedna. Alat (GitHub Actions) je samo način da se praksa provede.

| Pojam | Što je | Kod nas |
| --- | --- | --- |
| **workflow** | jedna YAML datoteka u `.github/workflows/` | `ci.yml` |
| **event** (`on`) | što pokreće workflow | PR, push na `main` |
| **job** | skupina koraka na **jednom** stroju; jobovi idu paralelno, osim ako ih ne povežeš s `needs` | `test`, `build` |
| **step** | jedna naredba (`run`) ili gotova akcija (`uses`) | `ruff check app` |
| **runner** | čisti virtualni stroj koji GitHub digne za svaki job i obriše nakon njega | `ubuntu-latest` |
| **action** | gotov, ponovno iskoristiv korak s GitHuba | `actions/checkout@v7` |

Najvažnija posljedica: runner je **prazan**. Nema tvog `.venv`-a, tvog `.env`-a ni imagea koje si buildao lokalno. Sve što pipeline treba mora biti u gitu ili se mora instalirati u samom workflowu. Zato CI hvata stvari poput „zaboravio sam dodati paket u `requirements-dev.txt`” (3. tjedan).

---

## 2. `ci.yml` linija po liniju

Gotov workflow je u [`.github/workflows/ci.yml`](../.github/workflows/ci.yml). Do 5. tjedna imao je samo job `test`. Ovaj tjedan dobiva `build`, cache i `concurrency`.

### 2.1 Kada se pokreće

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]
```

- **`pull_request`** — na svaki PR i na svaki novi push na granu tog PR-a. To je provjera **prije** mergea.
- **`push: branches: [main]`** — i nakon mergea, jer `main` sada sadrži kombinaciju koda koju PR nije vidio ako je u međuvremenu netko drugi mergeao.
- Workflow na feature grani radi **odmah**. Ne treba prvo biti na `main`.

### 2.2 Ne troši minute na zastarjele runove

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

Ako pushaš tri commita zaredom, bez ovoga se pokrenu tri runa i svi troše minute. `concurrency` drži najviše jedan run po grani (`github.ref`) i otkaže stariji kad stigne noviji.

### 2.3 Job `test`

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: app/requirements*.txt

      - name: Install dependencies
        run: pip install -r app/requirements-dev.txt

      - name: Lint
        run: ruff check app

      - name: Test
        run: python -m pytest -q
```

- **`actions/checkout`** — runner je prazan, pa prvi korak skoro uvijek preuzme kod iz repozitorija.
- **`uses` vs `run`.** `uses` poziva gotovu akciju (kod nekog drugog, s verzijom iza `@`), a `run` izvršava shell naredbu, istu kakvu bi upisao u terminal.
- **`cache: pip`** — `setup-python` sprema pip cache između runova. Ključ je sažetak datoteka iz `cache-dependency-path`: dok se `requirements*.txt` ne promijene, paketi se ne skidaju ponovno.
- **Lint pa test.** Koraci idu redom, a prvi koji vrati exit code različit od 0 zaustavlja job. Isti princip kao `set -e` u bashu (2. tjedan).
- Testovi ne trebaju ni bazu ni Redis, jer ih `conftest.py` zamjenjuje SQLiteom i fakeredisom (3. tjedan). Zato `test` job ne treba Compose.

### 2.4 Job `build`

```yaml
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - uses: docker/setup-buildx-action@v4

      - name: Build image
        uses: docker/build-push-action@v7
        with:
          context: ./app
          push: false
          build-args: APP_VERSION=${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

- **`needs: test`** — `build` čeka da `test` prođe. Bez `needs` jobovi idu **paralelno**, pa bi se image buildao i kad testovi padnu. To bi bilo bespotrebno trošenje minuta.
- **Svaki job je novi stroj**, pa i `build` mora napraviti `checkout`.
- **`setup-buildx-action`** — postavi BuildKit builder koji zna spremati cache izvan runnera.
- **`context: ./app`** — isto što i `docker build app` lokalno (4. tjedan): mapa u kojoj su `Dockerfile` i kod.
- **`push: false`** — ovaj tjedan samo provjeravamo da se image **može** buildati. Objava u registry (GHCR) dolazi u 7. tjednu.
- **`build-args: APP_VERSION=${{ github.sha }}`** — `GET /` u imageu pokazuje commit iz kojeg je buildan. `${{ … }}` su izrazi GitHub Actionsa i zamjenjuju se **prije** nego što se korak pokrene.
- **`cache-from` / `cache-to: type=gha`** — Docker slojevi iz 4. tjedna spremaju se u GitHub Actions cache. Ako se `requirements.txt` nije promijenio, sloj s `pip install` dolazi iz cachea. Isto kao `CACHED` lokalno, samo između runova na različitim strojevima. `mode=max` sprema i slojeve iz `builder` faze multi-stage builda.

> Brojevi iza `@` su **major verzije** akcija. Stare verzije (`checkout@v3`, `setup-python@v4`) rade na zastarjelom Node.js runtimeu i GitHub ih gasi. Ako ti AI predloži workflow, prvo provjeri verzije na stranici akcije (*Releases*).

---

## 3. Crveni pipeline

Pipeline je koristan tek kad **ne prođe**. Probaj namjerno:

```bash
git switch -c demo-red-ci
# u app/tests/test_health.py promijeni očekivani status 200 u 201
git commit -am "test: break health test on purpose"
git push -u origin demo-red-ci
gh pr create --fill
```

Na PR-u se pojavi crveni `CI / test`, a `build` je preskočen (*skipped*) zbog `needs`. Merge gumb je blokiran ako je `test` required check (poglavlje 4).

**Kako čitati log:** *Actions* → run → job `test` → otvori korak s crvenim ✗. Traži **prvu** grešku, ne zadnju. pytest na kraju ispiše sažetak (`FAILED app/tests/test_health.py::… assert 200 == 201`).

```bash
gh run list                    # zadnji runovi
gh run view --log-failed       # samo log koraka koji je pao
```

**Popravak** ide na **istu granu**: novi commit, push, PR se sam ažurira i CI se ponovno pokreće. Ne otvaraš novi PR.

**Reproduciraj lokalno prije pusha.** Ako CI pada, a ti ne znaš zašto, pokreni iste naredbe kao i on:

```bash
make lint && make test           # job test
docker build -t shortener app    # job build
```

---

## 4. Required checks: CI koji stvarno blokira

Crveni CI bez branch protectiona samo je upozorenje: merge gumb i dalje radi. U 3. tjednu `main` je zaštićen i traži `test`. Sad dodaj i `build`:

Settings → Branches → pravilo za `main` → **Require status checks to pass** → potraži i dodaj **`build`** (uz postojeći `test`).

- Check se u popisu pojavi tek kad se workflow s tim jobom **jednom pokrene**. Zato prvo otvori PR s novim `ci.yml`, pa tek onda podesi pravilo.
- Ime checka je ime **joba** (`build`), ne ime workflowa ni koraka. Ako job preimenuješ, required check treba ponovno odabrati, inače PR zauvijek čeka check koji više ne postoji (*Expected — Waiting for status to be reported*).

---

## 5. Minute

Na privatnim repozitorijima GitHub Free ima ograničen broj minuta Actionsa mjesečno, a Student Developer Pack (GitHub Pro) daje više. Jedan run našeg CI-ja traje oko minutu do dvije. To je dovoljno za cijeli semestar ako ne radiš ovo:

- `on: push` bez filtera grana: svaki push na svaku granu pokrene run, **plus** još jedan za PR,
- workflow koji se vrti na rasporedu (`schedule`) svakih nekoliko minuta,
- dugi `sleep` ili beskonačna petlja u koraku (dodaj `timeout-minutes: 10` jobu ako nisi siguran).

Potrošnja: Settings (tvog računa) → Billing and plans → *Usage this month*.

---

## 6. AI kutak: workflow uz AI

Zamoli AI alat da napiše CI workflow za tvoj stack (lint, testovi, build imagea na svaki PR). Zatim ga **pročitaj liniju po liniju** prije nego što ga commitaš i provjeri:

- **Verzije akcija.** AI često predloži `@v3` ili `@v4` jer ih je najviše vidio u podacima za učenje. Usporedi s *Releases* stranicom akcije.
- **`context` i putanje.** Je li `Dockerfile` stvarno tamo gdje workflow misli (`./app`, `./backend`, `.`)?
- **`push: true`.** Na PR-u ne treba objavljivati image, a bez prijave u registry korak svejedno pada.
- **Tajne.** Nikad `password: mojalozinka` u YAML-u. Tajne idu u *Settings → Secrets* (7. tjedan) i čitaju se kao `${{ secrets.IME }}`.
- **Okidači.** `on: [push, pull_request]` bez filtera radi dvostruke runove (poglavlje 5).

Ako workflow pada, daj AI-ju **log koraka koji je pao** (`gh run view --log-failed`), a ne samo „ne radi”. Prije lijepljenja provjeri da u logu nema tajni. Zapiši u [`docs/ai-log.md`](ai-log.md) što je AI predložio i što si morao ispraviti.

---

## 7. Zadatak `lab-06`

Na grani `lab-06-…`, kao PR s labelom `lab-06`:

**Kriteriji prihvaćanja:**

- [ ] `.github/workflows/ci.yml` s jobom `test`: lint i testovi tvoje aplikacije
- [ ] job `build` koji builda Docker image tvog API-ja (`push: false`)
- [ ] `build` ima `needs: test`
- [ ] cache: pip (ili ekvivalent za tvoj jezik) i Docker slojevi (`type=gha`)
- [ ] na PR-u `lab-06` oba joba su zelena
- [ ] branch protection na `main` traži **oba** checka (`test` i `build`)
- [ ] u opisu PR-a: poveznica na jedan **crveni** run (namjerno slomljen test ili lint) i kratko objašnjenje što je log pokazao
- [ ] ako si koristio AI, zapis u `docs/ai-log.md`

| Bodovi | Kriterij |
| --- | --- |
| 3 | lint + testovi + build, `needs`, cache, oba joba su required checks |
| 2 | build radi, ali nije required check **ili** nema cachea |
| 1 | workflow postoji, ali build ne prolazi |
| 0 | nema build joba |

**Rok:** početak sljedećeg termina (računa se otvaranje PR-a). Od ovog tjedna PR se mergea tek kad je CI zelen ([lab-submission](lab-submission.md)).

---

## Česte greške

- **YAML indentacija.** `steps:` uvučen krivo, ili tab umjesto razmaka. GitHub javi *Invalid workflow file* i ne pokrene ništa. Ekstenzija *GitHub Actions* za VS Code ili [`actionlint`](https://github.com/rhysd/actionlint) to hvata prije pusha.
- **Workflow u krivoj mapi.** Mora biti točno `.github/workflows/*.yml`. `.github/workflow/` ili `github/workflows/` se tiho ignoriraju.
- **`ModuleNotFoundError` u CI-ju, a lokalno radi.** Paket je instaliran u tvoj `.venv`, ali nije u `requirements*.txt`. Runner je prazan i zna samo ono što je u gitu.
- **`failed to read dockerfile`.** Kriv `context`: tvoj `Dockerfile` nije u `./app`. Putanje su relativne na korijen repozitorija.
- **Testovi u CI-ju traže pravu bazu** (`connection refused` na `localhost:5432`). Testovi ne smiju ovisiti o servisima koji ne postoje na runneru. Zamijeni ih kao u `conftest.py` (3. tjedan) ili ih u CI-ju preskoči.
- **Required check `build` se ne nudi u postavkama.** Workflow s tim jobom se još nije nijednom pokrenuo. Prvo PR, pa pravilo.
- **PR zauvijek čeka check.** Required check ima ime joba koji više ne postoji (preimenovan ili obrisan). Ažuriraj pravilo u branch protectionu.
- **Image se builda svaki put ispočetka.** Fali `cache-from`/`cache-to` ili `setup-buildx-action` (bez Buildxa `type=gha` cache ne radi).
