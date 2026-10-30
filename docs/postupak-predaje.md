# Postupak predaje laba

Jedan lab = **jedna grana + jedan pull request s labelom `lab-XX`**. Sve naredbe pokrećeš u korijenu svog repozitorija.

> Cijeli postupak je stvarno proveden na primjeru `lab-02`: [PR #1](https://github.com/vanjaluk8/praktikum-demo-app/pull/1) (`scripts/backup-docs.sh`). Otvori ga i vidi kako izgleda gotov PR.

## 1. Kreni od svježeg `main`-a

```bash
git switch main
git pull
git switch -c lab-06-ci
```

Ime grane: `lab-XX-kratki-opis`. Nikad ne radi izravno na `main`.

## 2. Napravi zadatak i provjeri ga

- kod ide u mapu koju zadatak traži (`scripts/`, `app/`, `.github/workflows/`…)
- pokreni ono što zadatak traži (`make test`, `make lint`, `./scripts/tvoja-skripta.sh`…)
- pogledaj što si promijenio:

```bash
git status
git diff
```

## 3. Commitaj

Koristi [Conventional Commits](https://www.conventionalcommits.org/): `tip: kratki opis`, engleski, malo slovo.

```bash
git add -A
git commit -m "ci: add docker build job"
```

Jedan commit = jedna logička promjena. Prije `git add -A` provjeri `git status` da slučajno ne dodaš `.env`.

## 4. Pošalji granu na GitHub

```bash
git push -u origin lab-06-ci
```

`-u` samo prvi put; poslije je dovoljno `git push`.

## 5. Napravi labelu (samo prvi put za taj lab)

GitHub → **Issues → Labels → New label** → ime `lab-06`.

Ili iz terminala:

```bash
gh label create lab-06 --color 0e8a16
```

## 6. Otvori pull request

GitHub: žuta traka **Compare & pull request** → base `main`, compare `lab-06-ci` → dodaj labelu `lab-06` → ispuni predložak.

Ili iz terminala:

```bash
gh pr create --base main --label lab-06 --fill
```

U opisu napiši što PR radi i kako si provjerio da radi. **Rok se računa po trenutku otvaranja PR-a**, ne mergea.

## 7. Pričekaj CI

Rezultat je na dnu PR-a (*Checks*) ili u kartici **Actions**.

Ako je crven, popravi na **istoj grani**:

```bash
git add -A
git commit -m "fix: correct image tag"
git push
```

PR se sam ažurira. Ne otvaraj novi PR.

## 8. Mergeaj sam

Kad je CI zelen → **Merge pull request**. Ne čekaš odobrenje nastavnika (Required approvals = 0).

Ili iz terminala:

```bash
gh pr merge --merge --delete-branch
```

## 9. Počisti lokalno

```bash
git switch main
git pull
git branch -d lab-06-ci    # ako je nisi obrisao u koraku 8.
```

## 10. AI log

Ako je AI napisao ili bitno promijenio nešto što predaješ, dodaj zapis u [`ai-log.md`](ai-log.md) i označi to u PR-u.

## Gotovo? Provjeri

- [ ] PR ima labelu `lab-XX` i otvoren je prije roka
- [ ] CI je zelen
- [ ] PR je mergean u `main`
- [ ] grana je obrisana
- [ ] `main` je povučen lokalno
- [ ] AI log je dopunjen (ako je AI korišten)

## Checkpoint (7. i 13. tjedan)

Checkpoint nije PR — to je **tag** na `main`:

```bash
git switch main && git pull
git tag checkpoint-1
git push origin checkpoint-1
```

`git push` **ne šalje tagove**, zato je `git push origin checkpoint-1` obavezan. Provjera: `git ls-remote --tags origin`.

## Česte greške

| Greška | Rješenje |
| --- | --- |
| `protected branch hook declined` | pushaš na `main`; napravi granu i PR |
| `The current branch has no upstream branch` | `git push -u origin <grana>` |
| PR nema labelu | dodaj je u desnom stupcu PR-a |
| CI je crven | popravi i pushaj na istu granu |
| zaboravio si `git pull` prije nove grane | `git switch main && git pull`, pa nova grana |
| tag nije na GitHubu | `git push origin <tag>` |

Detaljnije: [`git-cheatsheet.md`](git-cheatsheet.md) · pravila i bodovanje: [`ocekivanja.md`](ocekivanja.md)
