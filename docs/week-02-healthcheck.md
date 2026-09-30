# 2. tjedan — Linux za ops: health check skripta

Ovaj tjedan pišemo prvu automatizaciju: skriptu koja provjerava rade li naši servisi, zapisuje rezultat u log i može se pokretati sama, bez nas, preko crona. Ista ideja, samo s drugim alatima, vratit će se kroz cijeli semestar: u Dockeru (5. tjedan), u Kubernetesu (10. tjedan) i u monitoringu (12. tjedan).

Na kraju ovog tjedna trebao bi znati:

- napisati bash skriptu koja ne "šuti" kad nešto pođe po zlu,
- objasniti što je exit code i zašto je važan,
- zakazati skriptu kroz cron i provjeriti je li se stvarno pokrenula,
- pronaći zašto servis ne radi pomoću logova i nekoliko osnovnih naredbi.

---

## 1. Zašto health check?

Servis može "raditi" (proces postoji) a da zapravo ne radi ništa korisno: zapeo je, izgubio vezu s bazom ili vraća greške. Zato svaki servis u našem projektu ima endpoint **`/health`** koji odgovara samo ako je servis stvarno spreman.

Naša skripta radi ono što će kasnije raditi Docker, Kubernetes i Prometheus: redovito "pita" svaki servis je li živ i reagira ako nije.

```bash
curl http://localhost:8000/health
# {"status":"ok","host":"..."}
```

---

## 2. Skripta korak po korak

Cijela skripta je u [`scripts/healthcheck.sh`](../scripts/healthcheck.sh). Ovdje su dijelovi koji su bitni.

### `set -euo pipefail` — skripta koja ne šuti

```bash
set -euo pipefail
```

Bash po defaultu nastavlja dalje i kad naredba padne. To je najčešći uzrok skripti koje "prođu", a zapravo nisu ništa napravile.

| Opcija | Što radi |
| --- | --- |
| `-e` | prekini skriptu čim neka naredba vrati grešku |
| `-u` | greška ako koristiš varijablu koja nije postavljena (tipfeler u imenu varijable) |
| `-o pipefail` | u `a \| b` greška u `a` se ne sakrije iza uspješnog `b` |

Ovo stavljamo na vrh **svake** skripte na kolegiju.

### Popis servisa

```bash
SERVICES=(
  "api=http://localhost:8000/health"
)
```

Servisi su u obliku `ime=url`. Sada imamo samo jedan, ali kad u 5. tjednu dođe `compose.yaml` s bazom i cacheom, samo dodajemo redove — skripta ostaje ista.

`"${entry%%=*}"` i `"${entry#*=}"` su bash parameter expansion: prvo vraća sve **prije** `=`, drugo sve **poslije**. Nema potrebe za `cut` ili `awk`.

### `curl` koji zna reći "ne"

```bash
curl -fsS --max-time 3 "$url"
```

| Opcija | Zašto |
| --- | --- |
| `-f` | HTTP 500 ili 404 tretira kao grešku. **Bez ovoga curl javlja uspjeh i kad servis vraća grešku.** |
| `-sS` | bez progress bara, ali ispiši grešku ako se dogodi |
| `--max-time 3` | ne čekaj zauvijek servis koji se objesio |

### Exit code — kako skripta javlja rezultat

```bash
exit $(( failed > 0 ))
```

Svaka naredba u Linuxu završava s brojem: **0 znači uspjeh, sve ostalo je greška.** Probaj:

```bash
./scripts/healthcheck.sh
echo $?        # 0 ako sve radi, 1 ako nešto ne radi
```

Ovo nije detalj. Cron, CI pipeline, Docker healthcheck i Kubernetes probe gledaju **isključivo exit code**, a ne ono što skripta ispiše. Skripta koja uvijek vrati 0 za njih je skripta kojoj je uvijek sve u redu.

### Log

```bash
echo "$(date '+%F %T') $name $status" | tee -a "$LOG"
```

`tee -a` ispisuje na ekran i istovremeno dopisuje u datoteku. Svaki zapis ima vrijeme, jer bez vremena log ne pomaže u istrazi.

```
2026-10-14 10:05:01 api OK
2026-10-14 10:10:01 api FAIL
```

---

## 3. Cron — neka skripta radi sama

Otvori svoj crontab:

```bash
crontab -e
```

i dodaj red:

```
*/5 * * * * /home/<tvoj-user>/praktikum/scripts/healthcheck.sh
```

Pet polja znače: minuta, sat, dan u mjesecu, mjesec, dan u tjednu. `*/5` u prvom polju = svakih 5 minuta. Za provjeru izraza koristi [crontab.guru](https://crontab.guru).

**Tri stvari na koje se svi spotaknu:**

1. **Apsolutne putanje.** Cron ne kreće iz tvog direktorija i nema tvoj `PATH`. `./scripts/healthcheck.sh` u crontabu neće raditi.
2. **Skripta mora biti izvršna:** `chmod +x scripts/healthcheck.sh`.
3. **U WSL-u cron po defaultu ne radi.** Pokreni ga s `sudo service cron start`, ili trajno uključi systemd dodavanjem u `/etc/wsl.conf`:
   ```ini
   [boot]
   systemd=true
   ```
   i restartaj WSL (`wsl --shutdown` u PowerShellu).

Je li se cron uopće pokrenuo?

```bash
grep CRON /var/log/syslog | tail
```

---

## 4. Troubleshooting — kad servis ne radi

Na vježbama ćemo namjerno srušiti API i proći kroz istragu kao u pravom incidentu.

1. **Simptom:** u logu se pojavi `FAIL`.
   ```bash
   tail -f ~/healthcheck.log
   ```
2. **Sluša li itko na portu?**
   ```bash
   ss -tlnp | grep 8000
   ```
   Ako je prazno, servis nije pokrenut ili sluša na drugom portu.
3. **Postoji li proces?**
   ```bash
   ps aux | grep uvicorn
   ```
4. **Što kaže sam servis?** Pogledaj ispis u terminalu gdje radi (ili njegov log). Tražimo zadnju grešku prije pada.
5. **Popravi, pokreni ponovno, provjeri** da se u logu opet pojavljuje `OK`.

Redoslijed je uvijek isti: **simptom → mreža → proces → logovi servisa → popravak → provjera.** Isti postupak koristit ćemo u 10. tjednu s `kubectl` i u 14. tjednu na simuliranom incidentu.

---

## 5. Zadatak `lab-02`

Napiši **vlastitu** bash skriptu za automatizaciju nečega korisnog u svom projektu i predaj je kao PR s labelom `lab-02` u mapu `scripts/`.

Ideje (ili smisli svoju):

- backup baze u datoteku s datumom u imenu i brisanje backupa starijih od 7 dana,
- čišćenje starih logova,
- provjera zauzeća diska s upozorenjem iznad praga,
- provjera jesu li instalirane sve potrebne verzije alata.

**Kriteriji prihvaćanja:**

- [ ] `set -euo pipefail` na vrhu
- [ ] smislen exit code: 0 za uspjeh, različito od 0 za grešku
- [ ] jasna poruka kad nešto pođe po zlu
- [ ] može se pokrenuti dvaput zaredom bez problema
- [ ] kratki komentar na vrhu: što skripta radi i kako se pokreće
- [ ] ako si koristio AI, zapis u `docs/ai-log.md`

Rok: početak sljedećeg termina.

---

## Za one koji žele više

- [ShellCheck](https://www.shellcheck.net) — zalijepi skriptu i dobiješ popis grešaka i loših praksi. Isplati se provući svaku skriptu kroz njega.
- [Bash strict mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/) — detaljnije o `set -euo pipefail`.
- `man bash`, sekcija *Parameter Expansion*.
