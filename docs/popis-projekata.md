# Popis projekata

Svaki student bira jednu aplikaciju s ovog popisa (ili predlaže svoju uz odobrenje nastavnika). Jedna aplikacija = jedan student, po principu **tko prvi prijavi, taj je dobije**.

## Aplikacija je u drugom planu

Na ovom kolegiju ne ocjenjuje se aplikacija, nego sve oko nje: Dockerfile, pipeline, deployment, monitoring i sigurnost. Zato:

- **Kod aplikacije smije biti jednostavan i smije biti generiran uz AI.** Jezgra aplikacije trebala bi se moći napisati u jednom popodnevu. Ako ne može, prevelika je.
- Aplikacije su birane tako da svaka ima **nešto zanimljivo za infrastrukturu**: pozadinski posao, stanje koje treba sačuvati, vršno opterećenje, vanjsku ovisnost koja pada. Stupac *Infra izazov* govori što ćeš na svojoj aplikaciji najviše vježbati.
- Jezik i framework biraš sam.

## Obavezno za svaku aplikaciju

- najmanje **3 komponente**: aplikacija, baza i barem jedan dodatni servis (cache, worker, message queue, object storage…)
- **`/health` endpoint** na svakom servisu koji ima HTTP
- barem nekoliko testova
- nešto što se može mjeriti (broj zahtjeva, trajanje posla, veličina reda) — trebat će za monitoring u 12. tjednu

## Težina

- ★ — jednostavna logika, standardne komponente; uz jednu dodatnu stavku po izboru s ★★★ popisa (npr. worker ili message queue)
- ★★ — pozadinski poslovi, zakazani zadaci ili vanjske ovisnosti
- ★★★ — skaliranje, stateful servisi ili stvarno vrijeme

---

## Popis

| # | Aplikacija | Komponente | Infra izazov | Težina | Prijavio |
| --- | --- | --- | --- | --- | --- |
| 1 | Pastebin s istekom zapisa | API, PostgreSQL, cron za čišćenje | Kubernetes CronJob, TTL podataka | ★ | |
| 2 | Kanban / upravljanje zadacima | frontend, API, baza, autentikacija | migracije baze u pipelineu, secrets | ★ | |
| 3 | Ankete i glasanje uživo | API, Redis brojači, frontend | rate limiting, opterećenje u trenutku glasanja | ★ | |
| 4 | Knjiga dojmova / guestbook s moderacijom | API, baza, worker za filtriranje | asinkroni posao, red čekanja | ★ | |
| 5 | Rezervacija termina (tereni, dvorane, konzultacije) | API, baza, worker za e-mail (Mailpit) | asinkroni poslovi, konfiguracija po okruženju | ★★ | |
| 6 | Posudba knjiga s podsjetnicima | API, baza, zakazani worker za obavijesti | zakazani poslovi, alert na neuspjeli posao | ★★ | |
| 7 | Rezultati i tablica amaterske lige | API, baza, cron koji puni podatke, frontend | cache, vršno opterećenje vikendom | ★★ | |
| 8 | RSS agregator vijesti | fetcher worker, baza, API, frontend | retry i backoff, praćenje grešaka vanjskih izvora | ★★ | |
| 9 | Praćenje cijena proizvoda | scheduler, scraper, baza, notifikacije | vanjske ovisnosti koje padaju, alerting | ★★ | |
| 10 | Uptime monitor / status stranica | checker worker, baza, javna status stranica | SLI/SLO, meta-monitoring (tko nadzire nadzornika) | ★★ | |
| 11 | Helpdesk / ticketing | frontend, API, baza, e-mail worker | RBAC, audit logovi, secrets | ★★ | |
| 12 | Digitalni jelovnik i narudžbe za kafić | web za goste, prikaz za šank, API, message queue | događaji u stvarnom vremenu, redovi poruka | ★★ | |
| 13 | Generator računa / PDF izvještaja | API, red poslova, PDF worker, object storage (MinIO) | skaliranje workera, pohrana artefakata | ★★ | |
| 14 | Servis za obradu slika (thumbnaili) | upload API, MinIO, RabbitMQ, worker | horizontalno skaliranje workera prema duljini reda (HPA) | ★★★ | |
| 15 | Chat u stvarnom vremenu | WebSocket servis, Redis pub/sub, baza | skaliranje stateful veza, sticky sessions | ★★★ | |
| 16 | Kviz uživo (Kahoot-stil) | WebSocket servis, Redis, API, frontend | kratki vršni skokovi prometa, load test | ★★★ | |
| 17 | Minimalni webshop | katalog, košarica, narudžbe, mock plaćanje | više mikroservisa, distribuirano praćenje (tracing) | ★★★ | |
| 18 | Telemetrija senzora (simulirani senzori temperature) | generator podataka, ingest API, TimescaleDB ili InfluxDB, Grafana | time-series podaci, retencija, dashboardi | ★★★ | |
| 19 | Praćenje gradskih autobusa (simulirani GPS) | simulator, ingest API, baza, karta na frontendu | stream podataka, latencija | ★★★ | |
| 20 | Pretraživač dokumenata | upload API, indekser, Meilisearch ili OpenSearch | stateful servis na Kubernetesu, backup indeksa | ★★★ | |
| 21 | Feature-flag servis | API, baza, mali klijent/SDK, admin sučelje | feature flags i canary (povezano sa 7. tjednom) | ★★★ | |
| 22 | RAG chatbot nad FAQ-om fakulteta | API, vektorska baza (pgvector ili Qdrant), lokalni LLM (Ollama) | resursi i limiti, monitoring LLM servisa (povezano s 14. tjednom) | ★★★ | |

**URL shortener nije na popisu** — to je ogledna aplikacija koju gradimo na vježbama.

---

## Vlastiti prijedlog

Može, uz odobrenje nastavnika do kraja 2. tjedna. U prijedlogu navedi:

1. što aplikacija radi (dvije rečenice),
2. koje su 3+ komponente,
3. što je na njoj zanimljivo za infrastrukturu (pozadinski posao, stanje, opterećenje, vanjska ovisnost).

Ako ne možeš odgovoriti na treće pitanje, aplikacija vjerojatno nije dobar izbor za ovaj kolegij.
