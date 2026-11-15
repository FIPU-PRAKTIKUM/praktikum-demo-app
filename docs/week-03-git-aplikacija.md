# 3. tjedan — Git i suradnja: prava aplikacija

Ovaj tjedan placeholder API zamjenjuješ **svojom aplikacijom** (API + baza + Redis) i od sada radiš kao u timu: svaka promjena ide preko grane i pull requesta, CI je provjeri, a `main` je zaključan za izravne pushove.

Na kraju ovog tjedna trebao bi znati:

- raditi na kratkoj grani i otvoriti pull request koji netko može pregledati,
- pisati commit poruke po Conventional Commits,
- ostaviti koristan code review (komentar na liniju, *Suggest changes*),
- uključiti branch protection na `main`,
- napisati `/health` koji stvarno provjerava ovisnosti i vraća `503` kad nešto ne radi.

---

## 1. Zašto grane i pull requesti?

U timu `main` mora **uvijek raditi** — iz njega se deploya. Zato nitko ne pusha izravno na `main`, nego:

1. napravi kratku granu (sati ili dan-dva, ne tjedni),
2. otvori pull request (PR),
3. CI pokrene testove, kolega pregleda kod,
4. tek tada merge.

To je **trunk-based development**: jedna glavna grana, puno malih PR-ova. Što je PR manji, lakše ga je pregledati i manja je šansa da nešto pukne.

Naredbe za cijeli postupak su u [git šalabahteru, poglavlje 3](git-cheatsheet.md#3-predaja-laba-svaki-tjedan). Ukratko:

```bash
git switch main && git pull
git switch -c lab-03-app
# ... radiš, commitaš ...
git push -u origin lab-03-app
# GitHub → Compare & pull request → labela lab-03
```

---

## 2. Commit poruke — Conventional Commits

`tip: kratki opis` — **na engleskom, malim slovom, bez točke na kraju**:

| Tip | Kada | Primjer |
| --- | --- | --- |
| `feat` | nova funkcionalnost | `feat: add /shorten endpoint` |
| `fix` | popravak greške | `fix: return 503 when redis is down` |
| `test` | testovi | `test: cover invalid url` |
| `docs` | dokumentacija | `docs: explain how to run the app` |
| `ci` | GitHub Actions | `ci: install requirements-dev.txt` |
| `chore` | ostalo | `chore: add .env.example` |

**Jedan commit = jedna logička promjena.** Primjer iz ogledne aplikacije — PR sa shortenerom ima pet commitova:

```
feat: add url shortener with postgres and redis
test: run tests without real database (sqlite + fakeredis)
ci: install requirements-dev.txt
docs: explain shortener and how to run it
docs: wait for postgres before make run
```

`update`, `fix` i `asdf` nisu poruke. Za tri mjeseca nećeš znati što si promijenio — a ni nastavnik na obrani.

---

## 3. Code review

Na PR-u otvori karticu **Files changed**:

- **Komentar na liniju:** prijeđi mišem preko broja linije → plavi `+` → napiši komentar.
- **Prijedlog izmjene:** u komentaru klikni ikonu ± (*Suggest changes*) i napiši kako bi linija trebala izgledati. Autor je može prihvatiti jednim klikom (*Commit suggestion*).
- Na kraju: **Review changes** → *Comment*.

Dobar review je konkretan: *"ovaj `except` guta svaku grešku — uhvati samo `redis.RedisError`"*, a ne *"izgleda ok"*.

**Peer review ovog tjedna:** dobit ćeš par. Vlasnik repozitorija doda kolegu kao collaboratora (repo je privatan, inače ga ne vidi). Reviewer ostavi **barem dva konkretna komentara** na `lab-03` PR — **samo komentira, ne commita** u tuđi repo.

---

## 4. Branch protection

Postavljaš jednom, na `main`:

**Settings → Branches → Add classic branch protection rule**

- **Branch name pattern:** `main`
- ☑ **Require a pull request before merging**
  - *Require approvals* **ostavi isključeno** — radiš sam i ne možeš odobriti vlastiti PR, pa bi se zaključao.
- ☑ **Require status checks to pass before merging**
  - u tražilicu upiši `test` i odaberi ga (to je job iz `.github/workflows/ci.yml`)
- ☑ **Do not allow bypassing the above settings**
- **Create**

Provjeri da radi:

```bash
git switch main
git commit --allow-empty -m "test: direct push"
git push
# remote: error: GH006: Protected branch update failed for refs/heads/main.
git reset --hard origin/main      # makni probni commit
```

**Zapinje li?**

| Problem | Rješenje |
| --- | --- |
| `test` se ne pojavljuje u popisu status checkova | CI se mora barem jednom pokrenuti. Otvori PR, pričekaj da CI završi, pa se vrati u postavke. |
| GitHub piše da pravila nisu primijenjena na privatnom repou (*Not enforced*, ponuda za Pro) | branch protection na privatnom repou traži GitHub Pro — dobiješ ga s [GitHub Educationom](github-education.md). Nije ti odobren? Javi se nastavniku. |
| PR se ne može mergeati: *Required status check "test" is expected* | CI još nije završio ili je crven. Pogledaj karticu **Checks**. |

---

## 5. Tvoja aplikacija

Minimum iz [popisa projekata](popis-projekata.md):

1. **API** — tvoja aplikacija, jezik i framework po izboru,
2. **baza** — PostgreSQL (ili druga),
3. **Redis** — cache, brojači, sesije…

…i uz to `/health` koji provjerava **obje veze** i nekoliko testova.

**Kako izgleda gotovo:** pogledaj [URL shortener u oglednoj aplikaciji](https://github.com/FIPU-PRAKTIKUM/praktikum-demo-app/tree/main/app) — cijela aplikacija je ~130 redova, a [README](https://github.com/FIPU-PRAKTIKUM/praktikum-demo-app/blob/main/app/README.md) objašnjava svaki dio.

### `/health` mora reći istinu

```python
@app.get("/health")
def health(response: Response) -> dict:
    # SELECT 1 na bazu, PING na Redis
    if not healthy:
        response.status_code = 503
```

Proces koji radi, a ne može do baze, **nije zdrav**. Skripte, Docker i Kubernetes gledaju samo **status kod** — `200` s porukom `"baza ne radi"` za njih znači "sve je u redu". Tvoja skripta iz 2. tjedna (`curl -f`) to odmah prepozna kao `FAIL`.

### Konfiguracija u `.env`, ne u kodu

Adresa baze, korisnik i lozinka dolaze iz varijabli okruženja. U `.env.example` (ide u git) napiši **koje** varijable trebaju, a stvarne vrijednosti drži u `.env` (u `.gitignore`).

```
POSTGRES_USER=app
POSTGRES_PASSWORD=promijeni-me
POSTGRES_DB=app
POSTGRES_HOST=localhost
REDIS_URL=redis://localhost:6379/0
```

### Baza i Redis do 5. tjedna: `docker run`

Compose stiže u 5. tjednu. Dotad ovisnosti dižeš ručno — službeni postgres image čita iste `POSTGRES_*` varijable, pa mu daš isti `.env`:

```bash
cp .env.example .env
docker run -d --name pg --env-file .env -p 5432:5432 postgres:16
docker run -d --name redis -p 6379:6379 redis:7
docker ps                                    # oba kontejnera Up
until docker exec pg pg_isready -h 127.0.0.1 -U app; do sleep 1; done
```

> **Pričekaj bazu prije `make run`.** Kontejner je *Up* nekoliko sekundi prije nego što PostgreSQL prima konekcije. Ako aplikacija krene prerano, pri startu padne s `OperationalError` i ostane mrtva (uz `--reload` proces radi, ali server ne). Tada: Ctrl+C, pričekaj bazu, ponovno `make run`. U 5. tjednu ovo čekanje preuzima Compose.

```bash
docker stop redis      # probaj: /health mora vratiti 503
docker start redis
docker rm -f pg redis  # kad završiš (podaci se brišu — volumeni su u 5. tjednu)
```

> Port `5432` je zauzet? Na računalu već radi lokalni PostgreSQL. Ugasi ga ili koristi `-p 5433:5432` i `POSTGRES_PORT=5433`.

### Testovi bez prave baze

CI nema PostgreSQL ni Redis. Zato testovi koriste zamjene: SQLite bazu u memoriji i [`fakeredis`](https://pypi.org/project/fakeredis/). Pogledaj [`app/tests/conftest.py`](https://github.com/FIPU-PRAKTIKUM/praktikum-demo-app/blob/main/app/tests/conftest.py) u oglednoj aplikaciji.

**Dodao si ovisnost za testove (npr. `fakeredis`)?** Stavi je u `app/requirements-dev.txt` i u `.github/workflows/ci.yml` promijeni instalaciju u:

```yaml
      - name: Install dependencies
        run: pip install -r app/requirements-dev.txt
```

Inače CI ne nađe paket, PR je crven i — s branch protectionom — **ne možeš mergeati**.

**Ne pišeš u Pythonu?** Prilagodi `Makefile` (`install`, `run`, `test`, `lint`) i korake u CI-ju. To je dio zadatka.

---

## 6. Zadatak `lab-03`

Na grani `lab-03-…`, kao PR s labelom `lab-03`:

**Kriteriji prihvaćanja:**

- [ ] placeholder je zamijenjen tvojom aplikacijom: **API + baza + Redis**
- [ ] `/health` provjerava bazu i Redis i vraća **`503`** kad neka ne radi
- [ ] `.env.example` s potrebnim varijablama; lozinke nisu u kodu ni u gitu
- [ ] testovi prolaze (`make test`) i **CI na PR-u je zelen**
- [ ] **branch protection** na `main` prema poglavlju 4
- [ ] više od jednog commita, poruke po Conventional Commits
- [ ] `README.md` (sekcija *Moj projekt*): kako pokrenuti aplikaciju i njezine ovisnosti
- [ ] ako si koristio AI, zapis u `docs/ai-log.md`
- [ ] **peer review:** barem dva konkretna komentara na PR-u dodijeljenog kolege

| Bodovi | Kriterij |
| --- | --- |
| 3 | sve iz kriterija prihvaćanja |
| 2 | nedostaje jedno (npr. nema branch protectiona ili `/health` ne provjerava ovisnosti) |
| 1 | aplikacija radi, ali ima manje od 3 komponente |
| 0 | placeholder nije zamijenjen |

**Rok:** početak sljedećeg termina (računa se otvaranje PR-a).

---

## Česte greške

- **Prevelika aplikacija.** Ako jezgru ne možeš napisati u jednom popodnevu, prevelika je. Ocjenjuje se infrastruktura oko nje.
- **`/health` uvijek vraća `200`.** Probaj: `docker stop redis`, pa `curl -i localhost:8000/health`.
- **Lozinka upisana u kod** kao zadana vrijednost. Završi u gitu, a u 13. tjednu je nađe gitleaks.
- **`.env` commitan.** Provjeri `git status` prije `git add -A`. Ako se dogodilo: [šalabahter, poglavlje 12](git-cheatsheet.md#12-kad-nešto-pođe-po-zlu).
- **Rad izravno na `main`** prije uključivanja zaštite. Nakon ovog tjedna to više nije moguće — i to je poanta.
