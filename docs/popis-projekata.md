# Popis projekata

Svaki student bira jednu aplikaciju s ovog popisa (ili predlaže svoju uz odobrenje nastavnika). Jedna aplikacija = jedan student, po principu **tko prvi prijavi, taj je dobije**.

## Aplikacija je u drugom planu

Na ovom kolegiju ne ocjenjuje se aplikacija, nego sve oko nje: Dockerfile, pipeline, deployment, monitoring i sigurnost. Svaka komponenta aplikacije znači još jedan Dockerfile, još jedan servis u composeu, još jedan Deployment i još jednu stvar koja može puknuti. **Zato je jednostavnija aplikacija bolji izbor.**

- **Kod aplikacije smije biti jednostavan i smije biti generiran uz AI.** Jezgra aplikacije trebala bi se moći napisati u jednom do dva popodneva.
- **Arhitektura mora stati na jedan slajd:** ako je ne možeš nacrtati s nekoliko kućica i strelica, prevelika je.
- **Cijeli stack mora raditi s 4 GB RAM-a.** U 11. i 12. tjednu na clusteru uz tvoju aplikaciju rade i Argo CD i Prometheus.
- Jezik i framework biraš sam. Frontend nije obavezan tamo gdje ne piše drugačije — dovoljan je API koji se može isprobati `curl`-om ili kroz `/docs`.
- **Minimalne funkcionalnosti su donja granica.** Ne dodaji ništa dok infrastruktura ne radi.

## Minimum za svaku aplikaciju

Tri komponente, najjednostavnije moguće:

1. **API** — tvoja aplikacija
2. **baza** — PostgreSQL (ili druga po izboru)
3. **Redis** — kao cache (ili za brojače, sesije…)

Uz to:

- **`/health` endpoint** koji provjerava i vezu prema bazi i Redisu
- barem nekoliko testova
- nešto što se može mjeriti (broj zahtjeva, cache hit rate, trajanje posla) — trebat će za monitoring u 12. tjednu

**Worker, message queue, object storage i slično nisu uvjet.** Kod ★★ aplikacija pozadinski posao je dio same ideje aplikacije i obično se pokreće iz istog koda kao zaseban proces.

## Težina

- ★ — API + baza + Redis, bez pozadinskih poslova. Najsigurniji izbor.
- ★★ — isto, plus jedan pozadinski ili zakazani posao, ili jedna vanjska ovisnost.
- ★★★ — samo za one koji žele više, uz odobrenje nastavnika. Vidi [zasebnu sekciju](#-za-napredne-uz-odobrenje).

---

## Pregled

| # | Aplikacija | Težina | Prijavio |
| --- | --- | --- | --- |
| 1 | [Pastebin s istekom zapisa](#1-pastebin-s-istekom-zapisa) | ★ | |
| 2 | [Kanban ploča](#2-kanban-ploča) | ★ | |
| 3 | [Ankete i glasanje](#3-ankete-i-glasanje) | ★ | |
| 4 | [Knjiga dojmova](#4-knjiga-dojmova) | ★ | |
| 5 | [Zbirka recepata](#5-zbirka-recepata) | ★ | |
| 6 | [Rezervacija termina](#6-rezervacija-termina) | ★★ | |
| 7 | [Posudba knjiga s podsjetnicima](#7-posudba-knjiga-s-podsjetnicima) | ★★ | |
| 8 | [Rezultati amaterske lige](#8-rezultati-amaterske-lige) | ★★ | |
| 9 | [RSS agregator vijesti](#9-rss-agregator-vijesti) | ★★ | |
| 10 | [Praćenje cijena proizvoda](#10-praćenje-cijena-proizvoda) | ★★ | |
| 11 | [Uptime monitor i status stranica](#11-uptime-monitor-i-status-stranica) | ★★ | |
| 12 | [Helpdesk](#12-helpdesk) | ★★ | |
| 13 | [Narudžbe za kafić](#13-narudžbe-za-kafić) | ★★ | |
| 14 | [Generator računa](#14-generator-računa) | ★★ | |

**URL shortener nije na popisu** — to je ogledna aplikacija koju gradimo na vježbama.

---

## ★ Jednostavne

### 1. Pastebin s istekom zapisa

Servis u koji korisnik zalijepi tekst ili kod i dobije kratki link za dijeljenje. Svaki zapis ima rok trajanja (1 sat, 1 dan, 1 tjedan), nakon kojeg više nije dostupan.

- **Minimalno:** `POST /pastes` (tekst + trajanje) → ID; `GET /pastes/{id}` → sadržaj ili 404 ako je istekao. Redis služi kao cache za često čitane zapise, a istek možeš riješiti i Redis TTL-om.
- **Komponente:** API, PostgreSQL, Redis.
- **Što vježbaš:** cache i TTL, metrika *cache hit rate*. Opcionalno: zakazani posao za brisanje isteklih zapisa iz baze kao Kubernetes `CronJob`.

### 2. Kanban ploča

Jednostavna ploča sa stupcima *To do*, *In progress* i *Done*, na kojoj korisnik stvara zadatke i premješta ih između stupaca.

- **Minimalno:** registracija i prijava; CRUD za zadatke; promjena statusa. Redis za sesije ili cache ploče.
- **Komponente:** API, PostgreSQL, Redis; frontend po želji.
- **Što vježbaš:** migracije baze kao korak u pipelineu, secrets (lozinka baze, JWT ključ) kroz Kubernetes Secrets, dva okruženja s različitom konfiguracijom.

### 3. Ankete i glasanje

Korisnik napravi anketu s nekoliko odgovora, podijeli link, a drugi glasaju i vide rezultate.

- **Minimalno:** stvaranje ankete; glasanje (jedan glas po korisniku ili IP-u); `GET` rezultata. Brojači glasova u Redisu, ankete i konačni rezultati u bazi.
- **Komponente:** API, PostgreSQL, Redis.
- **Što vježbaš:** rate limiting, jednostavan load test (`hey` ili `k6`), što se dogodi s glasovima kad se Redis restartira.

### 4. Knjiga dojmova

Javna stranica na koju posjetitelji ostavljaju kratke poruke. Poruke se prije objave provjeravaju na zabranjene riječi i duljinu.

- **Minimalno:** `POST` poruke s provjerom; `GET` zadnjih N objavljenih poruka iz Redis cachea; brisanje poruke (admin).
- **Komponente:** API, PostgreSQL, Redis.
- **Što vježbaš:** invalidacija cachea kad stigne nova poruka, metrika "odbijenih poruka", konfiguracija popisa zabranjenih riječi kroz ConfigMap.

### 5. Zbirka recepata

Zbirka recepata s pretragom po sastojku i popisom najgledanijih recepata.

- **Minimalno:** CRUD recepata (naziv, sastojci, upute); pretraga po sastojku; "najpopularniji" recepti iz Redis brojača pregleda.
- **Komponente:** API, PostgreSQL, Redis.
- **Što vježbaš:** caching, početni podaci (seed) kao dio deploymenta, backup i vraćanje baze.

---

## ★★ Srednje

### 6. Rezervacija termina

Sustav za rezervaciju termina (teniski tereni, dvorane, konzultacije). Korisnik vidi slobodne termine, rezervira jedan i dobije potvrdu.

- **Minimalno:** popis resursa i slobodnih termina; rezervacija bez dvostrukog bukiranja; potvrda e-mailom iz pozadinskog posla.
- **Komponente:** API, PostgreSQL, Redis (lock za termin ili red poslova), [Mailpit](https://mailpit.axllent.org/) kao lažni mail server.
- **Što vježbaš:** pozadinski posao, konfiguracija po okruženju (dev šalje u Mailpit), SMTP podaci kao secret.

### 7. Posudba knjiga s podsjetnicima

Mala knjižnica: evidencija knjiga i posudbi, s automatskim podsjetnikom prije roka za vraćanje.

- **Minimalno:** CRUD knjiga i članova; posudba i vraćanje; dnevni zakazani posao koji šalje podsjetnike (e-mail u Mailpit ili zapis u log).
- **Komponente:** API, PostgreSQL, Redis, zakazani posao.
- **Što vježbaš:** Kubernetes `CronJob`, idempotentnost (podsjetnik se ne smije poslati dvaput ako posao krene ponovno), alert kad posao ne prođe.

### 8. Rezultati amaterske lige

Stranica s rezultatima i tablicom jedne amaterske lige (nogomet, košarka, pikado…).

- **Minimalno:** ekipe, utakmice i rezultati; automatski izračun tablice; tablica u Redis cacheu koji se poništava kad stigne novi rezultat; zakazani uvoz rezultata iz CSV-a.
- **Komponente:** API, PostgreSQL, Redis, zakazani posao.
- **Što vježbaš:** caching i invalidacija, usporedba latencije s cacheom i bez njega na dashboardu.

### 9. RSS agregator vijesti

Aplikacija koja periodično povlači RSS feedove s nekoliko portala i prikazuje članke na jednom mjestu.

- **Minimalno:** popis feedova; pozadinski posao koji svakih N minuta povlači nove članke bez duplikata; `GET` članaka s filtriranjem po izvoru.
- **Komponente:** API, PostgreSQL, Redis, fetcher posao.
- **Što vježbaš:** vanjski izvori koji ne rade ili su spori — timeout, retry i backoff; metrika "uspješnih / neuspjelih dohvaćanja po izvoru".

### 10. Praćenje cijena proizvoda

Korisnik doda proizvod i ciljanu cijenu, a sustav periodično provjerava cijenu i javi kad padne ispod cilja.

- **Minimalno:** dodavanje proizvoda za praćenje; zakazani posao koji provjerava cijene; povijest cijena; obavijest (Mailpit ili zapis u log).
- **Komponente:** API, PostgreSQL, Redis, zakazani posao. Izvor cijena je **lažni katalog koji sam napraviš** (jedan endpoint koji nasumično mijenja cijene), a ne scraping stvarnih trgovina.
- **Što vježbaš:** ovisnost o vanjskom servisu koji ponekad ne radi, alerting, graf povijesti cijena u Grafani.

### 11. Uptime monitor i status stranica

Mali klon status stranice: korisnik doda URL-ove, sustav ih redovito provjerava i prikazuje dostupnost.

- **Minimalno:** popis URL-ova; pozadinski posao koji ih provjerava svakih 30–60 s; postotak dostupnosti za zadnjih 24 h; javna status stranica ili endpoint.
- **Komponente:** API, PostgreSQL, Redis (zadnji status), checker posao.
- **Što vježbaš:** SLI i SLO u najčišćem obliku; alert kad sam checker prestane raditi. Nastavak ideje health check skripte iz 2. tjedna.

### 12. Helpdesk

Sustav za prijavu problema: korisnik otvori ticket, agent ga preuzme i rješava.

- **Minimalno:** dvije uloge (korisnik i agent); otvaranje, dodjela i zatvaranje ticketa; komentari; e-mail obavijest o promjeni statusa iz pozadinskog posla.
- **Komponente:** API, PostgreSQL, Redis, Mailpit.
- **Što vježbaš:** role i ovlasti (RBAC) u aplikaciji i usporedba s RBAC-om u Kubernetesu, audit log, više secreta.

### 13. Narudžbe za kafić

Gost naruči s jelovnika preko linka za svoj stol, a narudžba se pojavi na popisu za šank. Konobar označi kad je gotova.

- **Minimalno:** jelovnik; narudžba po stolu; endpoint za šank koji vraća otvorene narudžbe (dovoljan je polling); promjena statusa narudžbe.
- **Komponente:** API, PostgreSQL, Redis (otvorene narudžbe); frontend po želji.
- **Što vježbaš:** vršno opterećenje u kratkom vremenu, što se dogodi s otvorenim narudžbama kad se API restartira, dvije replike API-ja.

### 14. Generator računa

Korisnik unese stavke računa, a sustav u pozadini generira PDF za preuzimanje.

- **Minimalno:** `POST` računa → posao u Redis redu; pozadinski posao generira PDF; `GET` statusa i preuzimanje PDF-a.
- **Komponente:** API, PostgreSQL, Redis (red poslova), PDF worker. PDF-ove spremaj u volume ili bazu; object storage (MinIO) je opcionalan.
- **Što vježbaš:** red poslova, trajanje posla kao metrika, PersistentVolume za generirane datoteke.

---

## ★★★ Za napredne, uz odobrenje

Ove aplikacije su zanimljive, ali svaka sama nosi velik dio semestra, a neke traže više RAM-a nego što stane uz ostatak stacka. Biraj ih samo ako si siguran u osnove i imaš jače računalo. **Prije odabira dogovori opseg s nastavnikom.**

| Aplikacija | Ukratko | Zašto je teško |
| --- | --- | --- |
| Obrada slika | upload → RabbitMQ → worker radi thumbnailove → MinIO | 5 komponenti, HPA prema duljini reda |
| Chat u stvarnom vremenu | sobe i poruke preko WebSocketa | skaliranje trajnih veza, Redis pub/sub između replika, WebSocket kroz ingress |
| Kviz uživo (Kahoot-stil) | sinkroni prikaz pitanja i rang-lista uživo | stanje igre, vršni skokovi prometa, WebSocket |
| Minimalni webshop | katalog, košarica, narudžbe kao zasebni servisi | 3+ servisa u svakom koraku (Dockerfile, chart, pipeline), tracing |
| Telemetrija senzora | simulirani senzori → ingest → time-series baza → Grafana | dodatna baza (TimescaleDB/InfluxDB), stalni dotok podataka |
| Praćenje gradskih autobusa | simulirani GPS → karta u stvarnom vremenu | stream podataka, frontend s kartom |
| Pretraživač dokumenata | upload → indeksiranje → pretraga | stateful search engine; OpenSearch traži puno RAM-a (Meilisearch je lakši) |
| Feature-flag servis | servis za uključivanje funkcionalnosti po korisniku | treba i demo klijent koji ga koristi; latencija kritična |
| RAG chatbot nad FAQ-om | lokalni LLM + vektorska baza | Ollama traži **16 GB+ RAM-a**; dugi zahtjevi i timeouti |

---

## Vlastiti prijedlog

Može, uz odobrenje nastavnika do kraja 2. tjedna. U prijedlogu navedi:

1. što aplikacija radi (dvije rečenice),
2. komponente (minimum: API + baza + Redis),
3. što je na njoj zanimljivo za infrastrukturu (cache, pozadinski posao, opterećenje, vanjska ovisnost).

Ako ne možeš odgovoriti na treće pitanje, aplikacija vjerojatno nije dobar izbor za ovaj kolegij.

## Ako ti kod aplikacije stvarno ne ide

Na zahtjev možeš dobiti **gotovu jednostavnu aplikaciju** od nastavnika i sav semestar raditi samo infrastrukturu oko nje. Ocjenjuje se ionako infrastruktura, pa to ne utječe na bodove — ali javi se do kraja 2. tjedna.
