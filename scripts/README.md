# scripts/

Pomoćne bash skripte za rad s projektom. Skripte ovdje su male, ali pišemo ih kao da će ih pokretati netko drugi, u 3 ujutro, bez nas pokraj sebe: moraju jasno reći što rade i glasno pasti kad nešto nije u redu.

| Skripta | Tjedan | Što radi |
| --- | --- | --- |
| `check-env.sh` | 1 | provjerava jesu li instalirani svi alati za kolegij (`make check`) |
| `healthcheck.sh` | 2, 5 | provjerava sve servise iz `compose.yaml`, zapisuje rezultat u log, vraća exit code |
| `backup-docs.sh` | 2 | arhivira `docs/` s datumom u imenu, briše arhive starije od 7 dana |

---

## `healthcheck.sh` — linija po liniju

Ispod je cijela skripta podijeljena u blokove. Brojevi redova odgovaraju datoteci, pa ih možeš pratiti u editoru.

> U 5. tjednu skripta je dobila bazu i Redis iz `compose.yaml` (redovi 9–10, 15–16 i 22–25). Verzija iz 2. tjedna, samo s `curl`-om: `git show week-02:scripts/healthcheck.sh`.

### Redovi 1–5: zaglavlje

```bash
1  #!/usr/bin/env bash
2  # Provjerava sve servise iz compose.yaml i zapisuje rezultat u log.
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

### Redovi 7–13: konfiguracija

```bash
 7  SERVICES=(
 8    "api=http://localhost:8000/health"
 9    "db=docker compose exec -T db pg_isready -h 127.0.0.1 -q"
10    "cache=docker compose exec -T cache redis-cli ping"
11  )
12  LOG="${LOG:-$HOME/healthcheck.log}"
13  failed=0
```

- **Redovi 7–11 — bash array.** Popis servisa u obliku `ime=provjera`. Konfiguracija je na vrhu skripte, odvojena od logike: kad dodamo servis, mijenjamo samo ovaj popis, a ostatak skripte ostaje isti.
  - **Provjera je URL** (red 8): skripta ga provjerava `curl`-om.
  - **Provjera je naredba** (redovi 9–10): baza i Redis ne govore HTTP, pa pitamo njihove vlastite alate. `docker compose exec` pokreće naredbu u kontejneru koji već radi; `-T` isključuje terminal, jer naredbu ne pokreće čovjek nego skripta ili cron. `pg_isready` i `redis-cli ping` vraćaju exit code 0 kad servis radi.
- **Red 12 — default vrijednost.** `${LOG:-...}` znači: ako je varijabla `LOG` postavljena, koristi nju, a ako nije, koristi `$HOME/healthcheck.log`. Tako skripta radi bez ikakvog podešavanja, a log se može preusmjeriti bez mijenjanja koda:
  ```bash
  LOG=/tmp/test.log ./scripts/healthcheck.sh
  ```
- **Red 13 — brojač.** Koliko servisa nije prošlo. Na kraju ga pretvaramo u exit code.

### Redovi 15–16: u korijen repozitorija

```bash
15  # docker compose traži compose.yaml, a cron ne kreće iz repozitorija.
16  cd "$(dirname "$0")/.."
```

- `docker compose` traži `compose.yaml` u **trenutnoj** mapi. Cron skriptu pokreće iz `$HOME` (2. tjedan, poglavlje 3), pa bi `docker compose exec` javio da nema projekta.
- **`$0`** je putanja do same skripte, `dirname` od nje uzme mapu (`scripts`), a `/..` je mapa iznad: korijen repozitorija. Skripta tako radi bez obzira odakle je pokrenuta.

### Redovi 18–20: petlja i rastavljanje zapisa

```bash
18  for entry in "${SERVICES[@]}"; do
19    name="${entry%%=*}"
20    check="${entry#*=}"
```

- **Red 18.** `"${SERVICES[@]}"` u navodnicima daje svaki element arraya kao zasebnu vrijednost, čak i ako sadrži razmake. Bez navodnika bash bi razbio elemente na razmacima — a naredbe u redovima 9–10 su pune razmaka.
- **Redovi 19–20 — parameter expansion.** Rastavljamo `api=http://...` na dva dijela bez pozivanja vanjskih alata:
  - `${entry%%=*}` — makni **najduži** dio s **kraja** koji odgovara `=*` → ostaje `api`
  - `${entry#*=}` — makni **najkraći** dio s **početka** koji odgovara `*=` → ostaje `http://localhost:8000/health`

  Mnemotehnika: `#` je na tipkovnici lijevo od `%`, pa `#` reže s lijeva, a `%` s desna.

> **Pitanje za razred:** zašto u redu 20 koristimo `#`, a ne `##`? (Pomoć: što ako URL sadrži `=`, npr. `?check=db`?)

### Redovi 22–25: URL postaje naredba

```bash
22    # URL provjerava curl, a sve ostalo je naredba koja vraća exit code.
23    if [[ $check == http* ]]; then
24      check="curl -fsS --max-time 3 $check"
25    fi
```

- **`[[ $check == http* ]]`** — u `[[ ]]` desna strana `==` je uzorak, pa `http*` znači „počinje s `http`”.
- Nakon ovog reda **svaka** provjera je naredba. Ostatak petlje više ne mora znati je li servis HTTP ili nešto drugo.
  - `-f` — HTTP 4xx i 5xx tretira kao grešku. **Najvažnija opcija u cijeloj skripti:** bez nje curl vraća 0 i kad servis odgovori s 500 Internal Server Error.
  - `-s` — bez progress bara. `-S` — ali ipak ispiši grešku ako se dogodi.
  - `--max-time 3` — ako servis ne odgovori u 3 sekunde, smatraj ga mrtvim. Bez toga skripta može visjeti zauvijek na servisu koji se objesio.

> **Probaj:** makni `-f` i pokreni skriptu protiv `http://localhost:8000/ne-postoji`. Što javlja skripta, a što `curl -i` na isti URL?

### Redovi 27–32: sama provjera

```bash
27    if bash -c "$check" >/dev/null 2>&1; then
28      status="OK"
29    else
30      status="FAIL"
31      failed=$((failed + 1))
32    fi
```

- **Red 27 — `if` na naredbi.** U bashu `if` ne provjerava izraz, nego **exit code naredbe**: 0 znači istina, sve ostalo laž.
  - `bash -c "$check"` izvrši tekst iz varijable kao naredbu. Provjere pišemo mi, u samoj skripti; nikad ne izvršavaj ovako tekst koji dolazi od korisnika.
  - `>/dev/null 2>&1` — odbaci i standardni izlaz (`1`) i greške (`2`). Zanima nas samo exit code, ne tijelo odgovora.
- **Zašto `set -e` ovdje ne prekine skriptu?** Naredba unutar `if` uvjeta je iznimka: `-e` se ne primjenjuje jer je greška očekivana i obrađena.
- **Red 31 — aritmetika.** `$(( ... ))` je aritmetičko proširenje. Pazi: `((failed++))` bi pod `set -e` srušio skriptu kad je `failed` 0, jer izraz s vrijednošću 0 vraća exit code 1. Zato koristimo dodjelu.

### Redovi 34–35: zapis u log

```bash
34    echo "$(date '+%F %T') $name $status" | tee -a "$LOG"
35  done
```

- **`$(date '+%F %T')`** — command substitution: izvrši naredbu i umetni njezin izlaz. `%F` je `2026-10-14`, `%T` je `10:05:01`. Format godina-mjesec-dan sortira se ispravno i kao tekst.
- **`tee -a "$LOG"`** — `tee` dijeli izlaz: ispisuje na ekran **i** zapisuje u datoteku. `-a` znači dopiši (append); bez njega svako pokretanje briše prethodni log.
- **Navodnici oko `"$LOG"`** — ako putanja ima razmak, bez navodnika bash bi je razbio u dva argumenta.

### Red 37: rezultat

```bash
37  exit $(( failed > 0 ))
```

- `failed > 0` unutar `$(( ))` daje `1` ako je istina i `0` ako nije. Dakle: **exit 0 kad sve radi, exit 1 kad bilo što ne radi.**
- Ovo je jedini dio skripte koji čitaju cron, CI i Kubernetes. Ispis na ekranu je za ljude, exit code je za strojeve.

```bash
./scripts/healthcheck.sh; echo "exit code: $?"
docker compose stop cache && ./scripts/healthcheck.sh; docker compose start cache   # cache FAIL → exit 1
```

> Ako skriptu zakazuješ kroz cron, `docker` mora biti u cronovom `PATH`-u. Na macOS-u je u `/usr/local/bin`, pa na vrh crontaba dodaj `PATH=/usr/local/bin:/usr/bin:/bin`.

---

## `backup-docs.sh` — linija po liniju

Drugi primjer za 2. tjedan. Ista pravila kao `healthcheck.sh`, ali rješava drugi tip zadatka: **backup s datumom u imenu i čišćenje starih kopija**. Dobar je uzor za `lab-02` jer pokazuje provjeru preduvjeta i sigurno ponovno pokretanje.

### Redovi 1–5: zaglavlje

```bash
1  #!/usr/bin/env bash
2  # Arhivira mapu docs/ u tar.gz s datumom u imenu i briše arhive starije od 7 dana.
3  # Pokretanje:  ./scripts/backup-docs.sh
4  # Exit code:   0 = arhiva je napravljena, 1 = greška (npr. ne postoji docs/)
5  set -euo pipefail
```

Isto kao u `healthcheck.sh`: shebang, tri reda komentara (što radi, kako se pokreće, što znači exit code) i strict mode.

### Redovi 7–9: konfiguracija

```bash
 7  SRC="${SRC:-docs}"
 8  DEST="${DEST:-$HOME/praktikum-backup}"
 9  KEEP_DAYS="${KEEP_DAYS:-7}"
```

- Svaka postavka ima **default vrijednost**, pa skripta radi bez podešavanja, a mijenja se iz okruženja bez diranja koda:
  ```bash
  SRC=app DEST=/tmp/backup KEEP_DAYS=0 ./scripts/backup-docs.sh
  ```
- `KEEP_DAYS=0` u probi briše sve starije od 0 dana — najbrži način da vidiš čišćenje.

### Redovi 11–14: provjera preduvjeta

```bash
11  if [ ! -d "$SRC" ]; then
12    echo "GREŠKA: mapa '$SRC' ne postoji — pokreni skriptu iz korijena repozitorija." >&2
13    exit 1
14  fi
```

- Provjera ide **prije** bilo kakvog rada. Bolje je glasno pasti odmah nego napraviti praznu arhivu.
- Poruka ide na **stderr** (`>&2`): stdout ostaje za strojni izlaz, a čovjek odmah vidi gdje je problem.
- `exit 1` je signal koji razumiju cron i CI. Bez njega bi skripta "uspjela" iako ništa nije napravila.

### Redovi 16–19: arhiva

```bash
16  mkdir -p "$DEST"
17  ARCHIVE="$DEST/$(basename "$SRC")-$(date '+%F').tar.gz"
18  tar -czf "$ARCHIVE" "$SRC"
19  echo "$(date '+%F %T') backup OK: $ARCHIVE"
```

- `mkdir -p` ne pada ako mapa već postoji — zato drugo pokretanje ne pravi grešku.
- `date '+%F'` u imenu daje `docs-2026-10-30.tar.gz`. Format **godina-mjesec-dan** sortira se ispravno i kao tekst.
- Dvostruko pokretanje istog dana **prepiše** istu arhivu, zato je skripta sigurna za ponovno pokretanje.
- `tar -czf`: `-c` stvori arhivu, `-z` gzip, `-f` piši u datoteku.

### Red 21: čišćenje starih arhiva

```bash
21  find "$DEST" -name '*.tar.gz' -type f -mtime +"$KEEP_DAYS" -print -delete
```

- `-mtime +7` znači datoteke starije od 7 dana, a `-type f` preskače mape.
- `-print -delete` prvo **ispiše** putanju, pa je obriše — u logu vidiš što je uklonjeno, a ne samo da je "nešto" nestalo.
- `find` vraća 0 i kad ništa ne nađe, pa skripta ne pada kad nema što obrisati.

### Red 23: rezultat

```bash
23  exit 0
```

Eksplicitan uspjeh. Ako `tar` ili `find` padnu, `set -e` prekida skriptu s njihovim exit codeom prije ovog reda.

> **Probaj:** pokreni skriptu dvaput zaredom i usporedi `ls -l $HOME/praktikum-backup`. Zatim je pokreni s `KEEP_DAYS=0` i pogledaj što se dogodi sa svježom arhivom.

---

## Pravila za skripte na kolegiju

1. Shebang `#!/usr/bin/env bash` i `set -euo pipefail` na vrhu.
2. Komentar: što radi, kako se pokreće, što znači exit code.
3. Konfiguracija na vrhu, logika ispod.
4. Varijable uvijek u navodnicima: `"$var"`.
5. Exit code 0 samo kad je sve stvarno prošlo.
6. Skripta mora biti izvršna: `chmod +x scripts/ime.sh`.
7. Provuci je kroz [ShellCheck](https://www.shellcheck.net) prije predaje.
