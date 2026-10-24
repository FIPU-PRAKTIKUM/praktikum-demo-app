# Git i GitHub — šalabahter

Sve git i GitHub naredbe koje koristiš na kolegiju, složene redom kojim ti trebaju. Kako se predaje i boduje piše u [`ocekivanja.md`](ocekivanja.md). Ovdje su samo naredbe.

> **Windows:** sve naredbe pokrećeš u **WSL2 (Ubuntu)** terminalu, a repozitorij držiš u Linux home mapi (`~/`), **ne** u `/mnt/c/...`.

---

## Sadržaj

1. [Jednokratno postavljanje (1. tjedan)](#1-jednokratno-postavljanje-1-tjedan)
2. [Svakodnevni rad](#2-svakodnevni-rad)
3. [Predaja laba (svaki tjedan)](#3-predaja-laba-svaki-tjedan)
4. [Grane](#4-grane)
5. [Pregled povijesti i promjena](#5-pregled-povijesti-i-promjena)
6. [Tagovi i checkpointi](#6-tagovi-i-checkpointi)
7. [Ogledna aplikacija (`praktikum-demo-app`)](#7-ogledna-aplikacija-praktikum-demo-app)
8. [Commit poruke](#8-commit-poruke)
9. [GitHub u pregledniku](#9-github-u-pregledniku)
10. [GitHub CLI (`gh`) — neobavezno](#10-github-cli-gh--neobavezno)
11. [GitHub Actions i GHCR](#11-github-actions-i-ghcr)
12. [Kad nešto pođe po zlu](#12-kad-nešto-pođe-po-zlu)
13. [Česte greške](#13-česte-greške)

---

## 1. Jednokratno postavljanje (1. tjedan)

### Tko si

```bash
git config --global user.name "Ime Prezime"
git config --global user.email "tvoj@email.com"     # isti mail kao na GitHubu
git config --global init.defaultBranch main
git config --global pull.rebase false               # git pull radi merge, bez pitanja
git config --global core.autocrlf input             # WSL: bez Windows line endinga (CRLF)
git config --global core.editor "code --wait"       # VS Code kao editor (ili nano)
git config --global --list                          # provjera
```

### SSH ključ (da ne upisuješ lozinku)

```bash
ssh-keygen -t ed25519 -C "tvoj@email.com"          # Enter, Enter, Enter
cat ~/.ssh/id_ed25519.pub                          # kopiraj cijeli red
```

GitHub → avatar → **Settings → SSH and GPG keys → New SSH key** → zalijepi.

```bash
ssh -T git@github.com                               # "Hi <username>! You've successfully authenticated"
```

### Tvoj repozitorij iz predloška

1. GitHub → **`praktikum-project-template`** → **Use this template → Create a new repository**.
2. Ime: **`praktikum-<prezime>`** (mala slova, bez dijakritika). Vidljivost: **Private**.
3. **Settings → Collaborators → Add people** → dodaj nastavnika.

```bash
cd ~
git clone git@github.com:<tvoj-username>/praktikum-<prezime>.git
cd praktikum-<prezime>
git remote -v                                       # origin pokazuje na tvoj repo
make check                                          # jesu li svi alati instalirani
```

> Kloniraj preko **SSH** adrese (`git@github.com:...`), ne HTTPS. HTTPS traži token pri svakom pushu.

---

## 2. Svakodnevni rad

```bash
git status                       # što je promijenjeno — pokreći često
git diff                         # promjene koje još nisu dodane
git diff --staged                # promjene koje su dodane i idu u commit

git add datoteka.py              # dodaj jednu datoteku
git add scripts/                 # dodaj mapu
git add -A                       # dodaj sve (prvo provjeri git status!)

git commit -m "feat: add /health endpoint"
git push                         # pošalji na GitHub
git pull                         # povuci promjene s GitHuba
```

Tijek: **promijeni → `git status` → `git add` → `git commit` → `git push`**.

---

## 3. Predaja laba (svaki tjedan)

Isti postupak od 2. do 14. tjedna. Primjer za 6. tjedan:

```bash
git switch main
git pull                                  # kreni od najnovijeg main-a
git switch -c lab-06-ci                   # nova grana za lab

# ... radiš, testiraš (make test) ...

git status
git add -A
git commit -m "ci: add docker build job"
git push -u origin lab-06-ci              # -u samo pri prvom pushu grane
```

Zatim na GitHubu:

1. **Compare & pull request** (žuta traka) → base: `main`, compare: `lab-06-ci`.
2. Dodaj labelu **`lab-06`** (desno → *Labels*). Ako ne postoji: *Issues → Labels → New label*.
3. Ispuni **PR template**.
4. Pričekaj **zeleni CI** (od 6. tjedna).
5. **Merge pull request** — mergeaš sam.

Nakon mergea:

```bash
git switch main
git pull                                  # main sad sadrži tvoj lab
git branch -d lab-06-ci                   # obriši lokalnu granu (neobavezno)
```

Popravak nakon otvaranja PR-a? Samo commitaj i pushaj na **istu granu** — PR se sam ažurira:

```bash
git add -A
git commit -m "fix: correct image tag"
git push
```

---

## 4. Grane

```bash
git branch                       # lokalne grane (* = trenutna)
git branch -a                    # i grane na GitHubu
git switch naziv-grane           # prebaci se na granu
git switch -c nova-grana         # napravi granu i prebaci se na nju
git branch -d naziv-grane        # obriši mergeanu granu
git fetch --prune                # osvježi popis grana s GitHuba
```

Na drugu granu ne možeš prijeći s nespremljenim promjenama? Privremeno ih makni:

```bash
git stash                        # spremi promjene na stranu
git switch main
git stash pop                    # vrati ih natrag
```

Main se promijenio dok si radio na grani:

```bash
git switch main && git pull
git switch lab-06-ci
git merge main                   # uvuci novi main u svoju granu
```

### Konflikt pri mergeu

```bash
git status                       # "both modified: datoteka"
```

Otvori datoteku i nađi oznake:

```text
<<<<<<< HEAD
tvoja verzija
=======
verzija s main-a
>>>>>>> main
```

Ostavi ono što treba, obriši sve tri oznake, zatim:

```bash
git add datoteka
git commit                       # završi merge
git merge --abort                # ...ili odustani od mergea
```

---

## 5. Pregled povijesti i promjena

```bash
git log --oneline                # kratka povijest
git log --oneline --graph --all  # s granama
git log -p datoteka              # sve promjene jedne datoteke
git show <sha>                   # što je promijenio jedan commit
git diff main..lab-06-ci         # razlika između dvije grane
git blame datoteka               # tko je i kad promijenio svaki red
```

---

## 6. Tagovi i checkpointi

**Tag je trajno ime za jedan commit.** Grana (`main`) se pomiče sa svakim novim commitom, a tag zauvijek pokazuje na isti commit. Zato je dobar za "snimku stanja": checkpoint na tvom repou, `week-XX` u oglednoj aplikaciji.

```
A ── B ── C ── D ── E   ← main (ide dalje)
     ↑         ↑
  week-01   week-02     (ostaju gdje su)
```

> **`git push` ne šalje tagove.** Tag postoji samo na tvom računalu dok ga izričito ne pushaš s `git push origin <ime-taga>`. Najčešći razlog "checkpoint nije predan".

Na GitHubu su tagovi pod **Code → Tags**. Uz svaki tag GitHub sam nudi **Source code (zip / tar.gz)**: to je automatski arhiv koda u tom stanju, ne trebaš ga ni raditi ni predavati.

Checkpoint 1 (7. tjedan) i checkpoint 2 (13. tjedan):

```bash
git switch main && git pull
git tag checkpoint-1
git push origin checkpoint-1
```

Provjera da je tag na GitHubu:

```bash
git tag                               # lokalni tagovi
git ls-remote --tags origin           # tagovi na GitHubu
```

Pomicanje taga **prije roka** (nakon roka se ne pomiče):

```bash
git tag -f checkpoint-1
git push -f origin checkpoint-1
```

---

## 7. Ogledna aplikacija (`praktikum-demo-app`)

Stanje nakon svake vježbe označeno je tagom `week-XX`. Ovdje ništa ne predaješ, samo gledaš.

```bash
git clone https://github.com/vanjaluk8/praktikum-demo-app.git
cd praktikum-demo-app

git pull --tags                  # povuci nove tjedne
git checkout week-05             # stanje nakon 5. tjedna
git diff week-04 week-05         # što je dodano u 5. tjednu
git diff week-04 week-05 --stat  # samo popis promijenjenih datoteka
git checkout main                # natrag na najnovije
```

Jedna datoteka iz određenog tjedna, bez prebacivanja:

```bash
git show week-05:compose.yaml
```

---

## 8. Commit poruke

Koristimo [Conventional Commits](https://www.conventionalcommits.org/): `tip: kratki opis` (engleski, malim slovom, bez točke).

| Tip | Kada | Primjer |
| --- | --- | --- |
| `feat` | nova funkcionalnost | `feat: add /shorten endpoint` |
| `fix` | popravak greške | `fix: return 503 when redis is down` |
| `docs` | dokumentacija | `docs: explain healthcheck script` |
| `test` | testovi | `test: cover invalid url` |
| `ci` | GitHub Actions | `ci: push image to ghcr` |
| `build` | Dockerfile, ovisnosti | `build: multi-stage dockerfile` |
| `chore` | ostalo (config, čišćenje) | `chore: add .env.example` |
| `refactor` | promjena koda bez promjene ponašanja | `refactor: extract db module` |

Jedan commit = jedna logička promjena. `"update"`, `"fix"` i `"asdf"` nisu poruke.

---

## 9. GitHub u pregledniku

| Što | Gdje |
| --- | --- |
| Dodati collaboratora | Settings → Collaborators → Add people |
| Branch protection (3. tjedan) | Settings → Branches → Add rule → `main` |
| Napraviti labelu | Issues → Labels → New label |
| Rezultat CI-ja | kartica **Actions**, ili dno PR-a (*Checks*) |
| Secrets za CI | Settings → Secrets and variables → Actions |
| Image u GHCR-u | profil → **Packages**, ili desni stupac repozitorija |
| Vidljivost repozitorija | Settings → General → Danger Zone |

**Branch protection za `main` (3. tjedan):**

- ✅ Require a pull request before merging — **Required approvals: 0**
- ✅ Require status checks to pass → odaberi `test`
- ✅ Do not allow bypassing the above settings

Provjera: `git push` izravno na `main` mora biti **odbijen**.

**Code review:** u PR-u kartica *Files changed* → klik na `+` pored reda → komentar ili *Suggest changes* → *Start a review* → *Submit review*.

---

## 10. GitHub CLI (`gh`) — neobavezno

Sve iz poglavlja 3 i 9 možeš i iz terminala. Instalacija: <https://cli.github.com>.

```bash
gh auth login                                  # jednom: GitHub.com → SSH → browser

gh repo view --web                             # otvori repo u pregledniku

gh label create lab-06 --color 0e8a16          # napravi labelu
gh pr create --fill --label lab-06             # otvori PR iz trenutne grane
gh pr view --web                               # otvori PR u pregledniku
gh pr checks                                   # stanje CI-ja za PR
gh pr merge --merge --delete-branch            # mergeaj i obriši granu
gh pr list                                     # otvoreni PR-ovi

gh run list                                    # zadnja pokretanja CI-ja
gh run watch                                   # prati CI uživo
gh run view --log-failed                       # log samo koraka koji je pao
```

---

## 11. GitHub Actions i GHCR

CI se pokreće sam na svaki push i PR (`.github/workflows/ci.yml`). Ponovno pokretanje: *Actions* → run → **Re-run jobs**.

Image iz GHCR-a (od 7. tjedna):

```bash
docker pull ghcr.io/<username>/<repo>:latest
docker run --rm -p 8000:8000 ghcr.io/<username>/<repo>:latest
curl localhost:8000/             # "version" = SHA commita
```

Privatni image traži prijavu. Napravi **Personal access token (classic)** s pravom `read:packages` (Settings → Developer settings → Personal access tokens):

```bash
echo <token> | docker login ghcr.io -u <username> --password-stdin
```

> Token **nikad** ne ide u git, u AI chat ni u screenshot.

---

## 12. Kad nešto pođe po zlu

| Situacija | Naredba |
| --- | --- |
| Odbaci promjene u datoteci (nije commitano) | `git restore datoteka` |
| Makni datoteku iz `git add` (ostaje promijenjena) | `git restore --staged datoteka` |
| Promijeni poruku zadnjeg commita (**prije** pusha) | `git commit --amend -m "nova poruka"` |
| Dodaj zaboravljenu datoteku u zadnji commit (**prije** pusha) | `git add datoteka && git commit --amend --no-edit` |
| Poništi zadnji commit, zadrži promjene (**prije** pusha) | `git reset --soft HEAD~1` |
| Poništi commit koji je već pushan | `git revert <sha>` pa `git push` |
| Radio si na `main` umjesto na grani (nije commitano) | `git switch -c lab-XX-naziv` — promjene idu s tobom |
| Commitao si na `main` umjesto na grani (nije pushano) | `git branch lab-XX-naziv`, `git reset --hard origin/main`, `git switch lab-XX-naziv` |
| Datoteka je već u gitu, a treba biti u `.gitignore` | dodaj u `.gitignore`, pa `git rm --cached datoteka` |
| Potpuno se izgubio | `git status` i `git log --oneline -5` — pa pitaj na forumu s outputom |

> **Oprez:** `git reset --hard` i `git push -f` brišu rad. Na granama koje su već na GitHubu koristi `git revert`. `git push -f` na kolegiju koristiš samo za pomicanje checkpoint taga.

### Commitao si lozinku ili token

1. **Odmah opozovi ili promijeni** secret — to je jedini korak koji stvarno pomaže.
2. Makni ga iz koda, stavi ga u `.env` (koji je u `.gitignore`) ili u GitHub Secrets.
3. Javi se nastavniku.

Brisanje u sljedećem commitu **nije dovoljno** — secret ostaje u povijesti (`git log -p`).

---

## 13. Česte greške

| Greška | Uzrok | Rješenje |
| --- | --- | --- |
| `Permission denied (publickey)` | SSH ključ nije dodan na GitHub | poglavlje 1, pa `ssh -T git@github.com` |
| `rejected ... (fetch first)` | na GitHubu ima commitova kojih lokalno nemaš | `git pull`, pa ponovo `git push` |
| `protected branch hook declined` | pushaš izravno na zaštićeni `main` | napravi granu i PR — to je namjerno |
| `The current branch has no upstream branch` | prvi push nove grane | `git push -u origin <grana>` |
| `Your local changes would be overwritten` | nespremljene promjene pri `switch`/`pull` | commitaj ili `git stash` |
| `detached HEAD` | napravio si `git checkout week-XX` ili SHA | `git switch main` |
| `bad interpreter: /bin/bash^M` | Windows line endings (CRLF) | `sed -i 's/\r$//' skripta.sh`; u VS Codeu dolje desno CRLF → LF |
| `.env` se pojavio u `git status` | nije u `.gitignore` | dodaj u `.gitignore`; ako je već commitan, `git rm --cached .env` i **promijeni secrete** |
| PR ne pokazuje nove commitove | pushao si na drugu granu | `git branch` — provjeri na kojoj si grani |
| `denied: permission_denied` pri pushu u GHCR | workflow nema `packages: write` | dodaj `permissions:` u workflow (7. tjedan) |
