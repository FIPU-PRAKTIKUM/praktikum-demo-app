# 2. tjedan — Linux za ops: health check skripta

Ovaj tjedan pišemo prvu automatizaciju: skriptu koja provjerava rade li naši servisi, zapisuje rezultat u log i može se pokretati sama, bez nas, preko crona. Ista ideja, samo s drugim alatima, vratit će se kroz cijeli semestar: u Dockeru (5. tjedan), u Kubernetesu (10. tjedan) i u monitoringu (12. tjedan).

Na kraju ovog tjedna trebao bi znati:

- napisati bash skriptu koja ne "šuti" kad nešto pođe po zlu,
- objasniti što je exit code i zašto je važan,
- zakazati skriptu kroz cron i provjeriti je li se stvarno pokrenula,
- pronaći zašto servis ne radi pomoću logova i nekoliko osnovnih naredbi.

---

## 0. Prije svega: digni API

Da bi imao što provjeravati, treba ti servis koji radi. U svom repozitoriju već ga imaš: placeholder API u `app/main.py` s endpointom `/health`. Treba mu samo Python okruženje.

**Jednom** (u rootu svog repozitorija):

```bash
make install                  # napravi .venv i instalira ovisnosti iz app/requirements-dev.txt
source .venv/bin/activate     # uključi venv; u promptu se pojavi (.venv)
make run                      # API na http://localhost:8000 — ovaj terminal ostavi otvoren
```

U **drugom terminalu** provjeri:

```bash
curl http://localhost:8000/health
# {"status":"ok","host":"..."}
```

Ugasiš ga s `Ctrl+C` u terminalu gdje radi.

**Na što paziti:**

- `source .venv/bin/activate` ponavljaš **u svakom novom terminalu** u kojem pokrećeš `make run` ili `make test`. Bez toga dobiješ `uvicorn: command not found`.
- `pip install` **bez venva** na Ubuntu 24.04 (default u WSL-u) javlja `externally-managed-environment`. To nije greška u tvom repou — sustav ne dopušta instalaciju Python paketa mimo `apt`-a. Zato venv.
- `python3 -m venv` javlja `ensurepip is not available`? Instaliraj ga: `sudo apt install -y python3-venv`.
- `.venv/` je u `.gitignore`, ne commitaš ga.

---

## 1. Zašto health check?

Servis može "raditi" (proces postoji) a da zapravo ne radi ništa korisno: zapeo je, izgubio vezu s bazom ili vraća greške. Zato svaki servis u našem projektu ima endpoint **`/health`** koji odgovara samo ako je servis stvarno spreman.

Naša skripta radi ono što će kasnije raditi Docker, Kubernetes i Prometheus: redovito "pita" svaki servis je li živ i reagira ako nije.

```bash
curl http://localhost:8000/health
# {"status":"ok","host":"..."}
```

---

## 2. Skripta

Cijela skripta je u [`scripts/healthcheck.sh`](../scripts/healthcheck.sh), a **objašnjenje linija po liniju** je u [`scripts/README.md`](../scripts/README.md). Ukratko, četiri ideje koje trebaš zapamtiti:

| Ideja | Gdje u skripti | Zašto |
| --- | --- | --- |
| Strict mode | `set -euo pipefail` | skripta glasno pada umjesto da tiho nastavi nakon greške |
| Konfiguracija odvojena od logike | array `SERVICES` na vrhu | novi servis = jedan novi red, logika se ne dira |
| `curl` koji zna reći "ne" | `curl -fsS --max-time 3` | bez `-f` curl javlja uspjeh i kad servis vraća 500 |
| Exit code | `exit $(( failed > 0 ))` | cron, CI, Docker i Kubernetes gledaju samo exit code, ne ispis |

Probaj odmah:

```bash
./scripts/healthcheck.sh
echo $?        # 0 ako sve radi, 1 ako nešto ne radi
```

Log izgleda ovako:

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

- backup baze u datoteku s datumom u imenu i brisanje backupa starijih od 7 dana (baza stiže tek u 3. tjednu — dotad možeš raditi backup bilo koje mape, npr. `docs/`),
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
