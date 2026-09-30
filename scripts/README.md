# scripts/

Pomoćne bash skripte za rad s projektom. Skripte ovdje su male, ali pišemo ih kao da će ih pokretati netko drugi, u 3 ujutro, bez nas pokraj sebe: moraju jasno reći što rade i glasno pasti kad nešto nije u redu.

| Skripta | Tjedan | Što radi |
| --- | --- | --- |
| `check-env.sh` | 1 | provjerava jesu li instalirani svi alati za kolegij (`make check`) |
| `healthcheck.sh` | 2 | provjerava `/health` svih servisa, zapisuje rezultat u log, vraća exit code |

---

## `healthcheck.sh` — linija po liniju

Ispod je cijela skripta podijeljena u blokove. Brojevi redova odgovaraju datoteci, pa ih možeš pratiti u editoru.

### Redovi 1–5: zaglavlje

```bash
1  #!/usr/bin/env bash
2  # Provjerava /health endpoint svakog servisa i zapisuje rezultat u log.
3  # Pokretanje:  ./scripts/healthcheck.sh
4  # Exit code:   0 = svi servisi rade, 1 = barem jedan ne radi
5  set -euo pipefail
```

- **Red 1 — shebang.** Govori sustavu kojim programom pokrenuti datoteku kad je pozoveš kao `./healthcheck.sh`. `/usr/bin/env bash` traži `bash` u `PATH`-u umjesto da pretpostavi `/bin/bash`, pa skripta radi i na macOS-u i na Linuxu. Bez shebanga skriptu pokreće tvoj trenutni shell, što može biti `zsh` ili `sh` s drugačijim ponašanjem.
- **Redovi 2–4 — komentar.** Tri stvari koje svatko treba znati prije pokretanja: što skripta radi, kako se pokreće i što znači rezultat. Ako komentar ne možeš napisati u tri reda, skripta vjerojatno radi previše.
- **Red 5 — strict mode.**
  - `-e`: prekini skriptu čim neka naredba vrati grešku.
  - `-u`: greška ako koristiš nepostavljenu varijablu. `rm -rf "$DIR/"` s pogrešno napisanim imenom varijable bez `-u` postaje `rm -rf /`.
  - `-o pipefail`: u `naredba1 | naredba2` greška prve naredbe se ne gubi iza uspjeha druge.

> **Probaj:** makni red 5 i u red 8 upiši nepostojeći URL s tipfelerom u imenu varijable. Što se promijeni?

### Redovi 7–12: konfiguracija

```bash
 7  SERVICES=(
 8    "api=http://localhost:8000/health"
 9    # 5. tjedan: ovdje dodajemo ostale servise iz compose.yaml
10  )
11  LOG="${LOG:-$HOME/healthcheck.log}"
12  failed=0
```

- **Redovi 7–10 — bash array.** Popis servisa u obliku `ime=url`. Konfiguracija je na vrhu skripte, odvojena od logike: kad dodamo servis, mijenjamo samo ovaj popis, a ostatak skripte ostaje isti.
- **Red 11 — default vrijednost.** `${LOG:-...}` znači: ako je varijabla `LOG` postavljena, koristi nju, a ako nije, koristi `$HOME/healthcheck.log`. Tako skripta radi bez ikakvog podešavanja, a log se može preusmjeriti bez mijenjanja koda:
  ```bash
  LOG=/tmp/test.log ./scripts/healthcheck.sh
  ```
- **Red 12 — brojač.** Koliko servisa nije prošlo. Na kraju ga pretvaramo u exit code.

### Redovi 14–16: petlja i rastavljanje zapisa

```bash
14  for entry in "${SERVICES[@]}"; do
15    name="${entry%%=*}"
16    url="${entry#*=}"
```

- **Red 14.** `"${SERVICES[@]}"` u navodnicima daje svaki element arraya kao zasebnu vrijednost, čak i ako sadrži razmake. Bez navodnika bash bi razbio elemente na razmacima.
- **Redovi 15–16 — parameter expansion.** Rastavljamo `api=http://...` na dva dijela bez pozivanja vanjskih alata:
  - `${entry%%=*}` — makni **najduži** dio s **kraja** koji odgovara `=*` → ostaje `api`
  - `${entry#*=}` — makni **najkraći** dio s **početka** koji odgovara `*=` → ostaje `http://localhost:8000/health`

  Mnemotehnika: `#` je na tipkovnici lijevo od `%`, pa `#` reže s lijeva, a `%` s desna.

> **Pitanje za razred:** zašto u redu 16 koristimo `#`, a ne `##`? (Pomoć: što ako URL sadrži `=`, npr. `?check=db`?)

### Redovi 18–23: sama provjera

```bash
18    if curl -fsS --max-time 3 "$url" >/dev/null 2>&1; then
19      status="OK"
20    else
21      status="FAIL"
22      failed=$((failed + 1))
23    fi
```

- **Red 18 — `if` na naredbi.** U bashu `if` ne provjerava izraz, nego **exit code naredbe**: 0 znači istina, sve ostalo laž. Ovdje je naredba `curl`.
  - `-f` — HTTP 4xx i 5xx tretira kao grešku. **Najvažnija opcija u cijeloj skripti:** bez nje curl vraća 0 i kad servis odgovori s 500 Internal Server Error.
  - `-s` — bez progress bara. `-S` — ali ipak ispiši grešku ako se dogodi.
  - `--max-time 3` — ako servis ne odgovori u 3 sekunde, smatraj ga mrtvim. Bez toga skripta može visjeti zauvijek na servisu koji se objesio.
  - `>/dev/null 2>&1` — odbaci i standardni izlaz (`1`) i greške (`2`). Zanima nas samo exit code, ne tijelo odgovora.
- **Zašto `set -e` ovdje ne prekine skriptu?** Naredba unutar `if` uvjeta je iznimka: `-e` se ne primjenjuje jer je greška očekivana i obrađena.
- **Red 22 — aritmetika.** `$(( ... ))` je aritmetičko proširenje. Pazi: `((failed++))` bi pod `set -e` srušio skriptu kad je `failed` 0, jer izraz s vrijednošću 0 vraća exit code 1. Zato koristimo dodjelu.

> **Probaj:** makni `-f` i pokreni skriptu protiv `http://localhost:8000/ne-postoji`. Što javlja skripta, a što `curl -i` na isti URL?

### Redovi 25–26: zapis u log

```bash
25    echo "$(date '+%F %T') $name $status" | tee -a "$LOG"
26  done
```

- **`$(date '+%F %T')`** — command substitution: izvrši naredbu i umetni njezin izlaz. `%F` je `2026-10-14`, `%T` je `10:05:01`. Format godina-mjesec-dan sortira se ispravno i kao tekst.
- **`tee -a "$LOG"`** — `tee` dijeli izlaz: ispisuje na ekran **i** zapisuje u datoteku. `-a` znači dopiši (append); bez njega svako pokretanje briše prethodni log.
- **Navodnici oko `"$LOG"`** — ako putanja ima razmak, bez navodnika bash bi je razbio u dva argumenta.

### Red 28: rezultat

```bash
28  exit $(( failed > 0 ))
```

- `failed > 0` unutar `$(( ))` daje `1` ako je istina i `0` ako nije. Dakle: **exit 0 kad sve radi, exit 1 kad bilo što ne radi.**
- Ovo je jedini dio skripte koji čitaju cron, CI i Kubernetes. Ispis na ekranu je za ljude, exit code je za strojeve.

```bash
./scripts/healthcheck.sh; echo "exit code: $?"
```

---

## Pravila za skripte na kolegiju

1. Shebang `#!/usr/bin/env bash` i `set -euo pipefail` na vrhu.
2. Komentar: što radi, kako se pokreće, što znači exit code.
3. Konfiguracija na vrhu, logika ispod.
4. Varijable uvijek u navodnicima: `"$var"`.
5. Exit code 0 samo kad je sve stvarno prošlo.
6. Skripta mora biti izvršna: `chmod +x scripts/ime.sh`.
7. Provuci je kroz [ShellCheck](https://www.shellcheck.net) prije predaje.
