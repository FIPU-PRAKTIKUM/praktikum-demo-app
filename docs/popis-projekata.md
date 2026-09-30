# Popis projekata

Svaki student bira jednu aplikaciju s ovog popisa (ili predlaže svoju uz odobrenje nastavnika). Jedna aplikacija = jedan student, po principu **tko prvi prijavi, taj je dobije**.

## Aplikacija je u drugom planu

Na ovom kolegiju ne ocjenjuje se aplikacija, nego sve oko nje: Dockerfile, pipeline, deployment, monitoring i sigurnost. Zato:

- **Kod aplikacije smije biti jednostavan i smije biti generiran uz AI.** Jezgra aplikacije trebala bi se moći napisati u jednom popodnevu. Ako ne može, prevelika je.
- Aplikacije su birane tako da svaka ima **nešto zanimljivo za infrastrukturu**: pozadinski posao, stanje koje treba sačuvati, vršno opterećenje, vanjsku ovisnost koja pada. U opisu svake aplikacije piše što ćeš na njoj najviše vježbati.
- Jezik i framework biraš sam. Frontend nije obavezan tamo gdje ne piše drugačije — dovoljan je API koji se može isprobati `curl`-om ili kroz `/docs`.
- **Minimalne funkcionalnosti** su donja granica. Ne dodaji više dok infrastruktura ne radi.

## Obavezno za svaku aplikaciju

- najmanje **3 komponente**: aplikacija, baza i barem jedan dodatni servis (cache, worker, message queue, object storage…)
- **`/health` endpoint** na svakom servisu koji ima HTTP, koji provjerava i veze prema ovisnostima (baza, cache)
- barem nekoliko testova
- nešto što se može mjeriti (broj zahtjeva, trajanje posla, veličina reda) — trebat će za monitoring u 12. tjednu

## Težina

- ★ — jednostavna logika, standardne komponente. Uz ★ projekt dodaj jednu stavku po izboru s ★★★ razine (npr. worker ili message queue).
- ★★ — pozadinski poslovi, zakazani zadaci ili vanjske ovisnosti.
- ★★★ — skaliranje, stateful servisi ili rad u stvarnom vremenu. Neki traže više RAM-a — to piše u opisu.

---

## Pregled

| # | Aplikacija | Težina | Prijavio |
| --- | --- | --- | --- |
| 1 | [Pastebin s istekom zapisa](#1-pastebin-s-istekom-zapisa) | ★ | |
| 2 | [Kanban ploča](#2-kanban-ploča) | ★ | |
| 3 | [Ankete i glasanje uživo](#3-ankete-i-glasanje-uživo) | ★ | |
| 4 | [Knjiga dojmova s moderacijom](#4-knjiga-dojmova-s-moderacijom) | ★ | |
| 5 | [Rezervacija termina](#5-rezervacija-termina) | ★★ | |
| 6 | [Posudba knjiga s podsjetnicima](#6-posudba-knjiga-s-podsjetnicima) | ★★ | |
| 7 | [Rezultati amaterske lige](#7-rezultati-amaterske-lige) | ★★ | |
| 8 | [RSS agregator vijesti](#8-rss-agregator-vijesti) | ★★ | |
| 9 | [Praćenje cijena proizvoda](#9-praćenje-cijena-proizvoda) | ★★ | |
| 10 | [Uptime monitor i status stranica](#10-uptime-monitor-i-status-stranica) | ★★ | |
| 11 | [Helpdesk](#11-helpdesk) | ★★ | |
| 12 | [Narudžbe za kafić](#12-narudžbe-za-kafić) | ★★ | |
| 13 | [Generator računa](#13-generator-računa) | ★★ | |
| 14 | [Obrada slika](#14-obrada-slika) | ★★★ | |
| 15 | [Chat u stvarnom vremenu](#15-chat-u-stvarnom-vremenu) | ★★★ | |
| 16 | [Kviz uživo](#16-kviz-uživo) | ★★★ | |
| 17 | [Minimalni webshop](#17-minimalni-webshop) | ★★★ | |
| 18 | [Telemetrija senzora](#18-telemetrija-senzora) | ★★★ | |
| 19 | [Praćenje gradskih autobusa](#19-praćenje-gradskih-autobusa) | ★★★ | |
| 20 | [Pretraživač dokumenata](#20-pretraživač-dokumenata) | ★★★ | |
| 21 | [Feature-flag servis](#21-feature-flag-servis) | ★★★ | |
| 22 | [RAG chatbot nad FAQ-om](#22-rag-chatbot-nad-faq-om) | ★★★ | |

**URL shortener nije na popisu** — to je ogledna aplikacija koju gradimo na vježbama.

---

## ★ Jednostavne

### 1. Pastebin s istekom zapisa

Servis u koji korisnik zalijepi tekst ili kod i dobije kratki link za dijeljenje. Svaki zapis ima rok trajanja (npr. 1 sat, 1 dan, 1 tjedan), nakon kojeg nestaje.

- **Minimalno:** `POST /pastes` (tekst + trajanje) → ID; `GET /pastes/{id}` → sadržaj ili 404 ako je istekao; zadatak koji periodično briše istekle zapise.
- **Komponente:** API, PostgreSQL, zakazani posao za čišćenje; ★ dodatak: Redis cache za često čitane zapise.
- **Što vježbaš:** zakazani posao kao Kubernetes `CronJob`, metrika "broj obrisanih zapisa", alert kad čišćenje ne prođe.

### 2. Kanban ploča

Jednostavna ploča sa stupcima *To do*, *In progress* i *Done*, na kojoj korisnik stvara zadatke i premješta ih između stupaca.

- **Minimalno:** registracija i prijava; CRUD za zadatke; promjena statusa; jednostavan frontend ili samo API.
- **Komponente:** API, PostgreSQL, frontend (ili API docs); ★ dodatak: worker koji šalje dnevni sažetak.
- **Što vježbaš:** migracije baze kao korak u pipelineu, secrets (lozinke, JWT ključ) kroz Kubernetes Secrets, dva okruženja s različitom konfiguracijom.

### 3. Ankete i glasanje uživo

Korisnik napravi anketu s nekoliko odgovora, podijeli link, a rezultati se osvježavaju dok ljudi glasaju.

- **Minimalno:** stvaranje ankete; glasanje (jedan glas po korisniku ili po IP-u); `GET` rezultata; brojači u Redisu, trajni zapis u bazi.
- **Komponente:** API, Redis, PostgreSQL; ★ dodatak: worker koji periodično prebacuje brojače iz Redisa u bazu.
- **Što vježbaš:** rate limiting, ponašanje pod naglim opterećenjem (load test s `hey` ili `k6`), što se dogodi s glasovima kad Redis padne.

### 4. Knjiga dojmova s moderacijom

Javna stranica na koju posjetitelji ostavljaju poruke. Svaka poruka prvo prolazi automatsku provjeru (zabranjene riječi, duljina, spam) i tek onda postaje vidljiva.

- **Minimalno:** `POST` poruke (odlazi u red); worker koji provjerava i odobrava ili odbija; `GET` odobrenih poruka.
- **Komponente:** API, PostgreSQL, message queue (Redis ili RabbitMQ), worker.
- **Što vježbaš:** asinkrona obrada, metrika "duljina reda", što se dogodi kad worker ne radi (poruke čekaju, ne gube se).

---

## ★★ Srednje

### 5. Rezervacija termina

Sustav za rezervaciju termina (teniski tereni, dvorane, konzultacije). Korisnik vidi slobodne termine, rezervira jedan i dobije potvrdu e-mailom.

- **Minimalno:** popis resursa i slobodnih termina; rezervacija bez dvostrukog bukiranja; potvrda e-mailom preko workera.
- **Komponente:** API, PostgreSQL, worker za e-mail, [Mailpit](https://mailpit.axllent.org/) kao lažni mail server.
- **Što vježbaš:** asinkroni poslovi, konfiguracija po okruženju (dev šalje u Mailpit, "prod" bi slao pravi mail), SMTP podaci kao secret.

### 6. Posudba knjiga s podsjetnicima

Mala knjižnica: evidencija knjiga i posudbi, s automatskim podsjetnikom nekoliko dana prije roka za vraćanje i upozorenjem kad rok istekne.

- **Minimalno:** CRUD knjiga i članova; posudba i vraćanje; dnevni zakazani posao koji šalje podsjetnike (e-mail u Mailpit ili zapis u log).
- **Komponente:** API, PostgreSQL, zakazani worker, Mailpit.
- **Što vježbaš:** zakazani poslovi, idempotentnost (podsjetnik se ne smije poslati dvaput ako posao krene ponovno), alert kad posao ne prođe.

### 7. Rezultati amaterske lige

Stranica s rezultatima, rasporedom i tablicom jedne amaterske lige (nogomet, košarka, pikado…). Rezultati se unose ručno ili ih periodično puni skripta.

- **Minimalno:** ekipe, utakmice i rezultati; automatski izračun tablice; cache tablice u Redisu koji se poništava kad stigne novi rezultat.
- **Komponente:** API, PostgreSQL, Redis, zakazani posao za uvoz rezultata (iz CSV-a ili lažnog izvora); frontend po želji.
- **Što vježbaš:** caching i invalidacija, vršno opterećenje nakon utakmica, usporedba latencije s cacheom i bez njega na dashboardu.

### 8. RSS agregator vijesti

Aplikacija koja periodično povlači RSS feedove s nekoliko portala, sprema članke i prikazuje ih na jednom mjestu, s pretragom po naslovu.

- **Minimalno:** popis feedova; worker koji svakih N minuta povlači nove članke bez duplikata; `GET` članaka s filtriranjem.
- **Komponente:** fetcher worker, PostgreSQL, API; frontend po želji.
- **Što vježbaš:** vanjski izvori koji ne rade ili su spori — retry, backoff i timeout; metrika "uspješnih / neuspjelih dohvaćanja po izvoru".

### 9. Praćenje cijena proizvoda

Korisnik doda proizvod (link ili lažni katalog) i ciljanu cijenu, a sustav periodično provjerava cijenu i javi kad padne ispod cilja.

- **Minimalno:** dodavanje proizvoda za praćenje; scheduler koji provjerava cijene; povijest cijena; obavijest (e-mail u Mailpit ili webhook).
- **Komponente:** scheduler/worker, PostgreSQL, API, notifikacije. Za izvor cijena preporuka je **lažni katalog koji sami napravite** (mali servis koji nasumično mijenja cijene), a ne scraping stvarnih trgovina.
- **Što vježbaš:** ovisnost o vanjskom servisu koji pada, alerting, graf povijesti cijena u Grafani.

### 10. Uptime monitor i status stranica

Mali klon status stranice: korisnik doda URL-ove, sustav ih redovito provjerava i prikazuje dostupnost i povijest ispada.

- **Minimalno:** popis URL-ova za praćenje; checker worker (svakih 30–60 s); postotak dostupnosti za zadnjih 24 h; javna status stranica.
- **Komponente:** checker worker, PostgreSQL, API, status stranica.
- **Što vježbaš:** SLI i SLO u najčišćem obliku; pitanje *tko nadzire nadzornika* — alert kad sam checker prestane raditi. Nastavak ideje health check skripte iz 2. tjedna.

### 11. Helpdesk

Sustav za prijavu problema: korisnik otvori ticket, agent ga preuzme i rješava, a korisnik dobiva obavijesti o promjeni statusa.

- **Minimalno:** dvije uloge (korisnik i agent); otvaranje, dodjela i zatvaranje ticketa; komentari; e-mail obavijest preko workera.
- **Komponente:** API, PostgreSQL, worker za e-mail, Mailpit; frontend po želji.
- **Što vježbaš:** role i ovlasti (RBAC) u aplikaciji i usporedba s RBAC-om u Kubernetesu, audit log, više secreta.

### 12. Narudžbe za kafić

Gost skenira QR kod na stolu, naruči s jelovnika, a narudžba se istog trena pojavi na ekranu za šankom. Konobar označi kad je gotova.

- **Minimalno:** jelovnik; narudžba po stolu; ekran za šank koji prima nove narudžbe (polling ili WebSocket); promjena statusa narudžbe.
- **Komponente:** web za goste, prikaz za šank, API, message queue (Redis ili RabbitMQ).
- **Što vježbaš:** događaji u gotovo stvarnom vremenu, message queue, što se dogodi s narudžbama kad se prikaz za šank restartira.

### 13. Generator računa

Korisnik unese stavke računa (kupac, artikli, cijene), a sustav u pozadini generira PDF i sprema ga za preuzimanje.

- **Minimalno:** `POST` računa → posao u redu; worker generira PDF; PDF se sprema u object storage; `GET` statusa i linka za preuzimanje.
- **Komponente:** API, PostgreSQL, red poslova, PDF worker, [MinIO](https://min.io/) kao S3-kompatibilan storage.
- **Što vježbaš:** skaliranje workera kad naraste red, pohrana artefakata izvan kontejnera, trajanje posla kao metrika.

---

## ★★★ Zahtjevne

### 14. Obrada slika

Korisnik uploada sliku, a sustav u pozadini napravi nekoliko verzija (thumbnail, srednja, WebP) i vrati linkove.

- **Minimalno:** upload; posao u RabbitMQ; worker koji generira verzije; spremanje u MinIO; `GET` statusa i linkova.
- **Komponente:** upload API, MinIO, RabbitMQ, worker, PostgreSQL za metapodatke.
- **Što vježbaš:** horizontalno skaliranje workera (HPA) kad naraste red, CPU limiti, load test s puno uploada.

### 15. Chat u stvarnom vremenu

Chat sa sobama: korisnici se spoje, uđu u sobu i razmjenjuju poruke u stvarnom vremenu. Povijest poruka ostaje sačuvana.

- **Minimalno:** WebSocket veza; sobe; slanje i primanje poruka; povijest zadnjih N poruka iz baze.
- **Komponente:** WebSocket servis, Redis pub/sub, PostgreSQL, jednostavan frontend.
- **Što vježbaš:** skaliranje servisa s trajnim vezama — kad pokreneš 2 replike, poruka mora stići i korisnicima spojenim na drugu repliku (zato Redis pub/sub); ingress i WebSocket.

### 16. Kviz uživo

Kahoot-stil kviz: voditelj pokrene kviz, igrači se spoje kodom, pitanja se prikazuju svima istovremeno, a rang-lista se osvježava nakon svakog pitanja.

- **Minimalno:** stvaranje kviza s pitanjima; spajanje igrača kodom; sinkroni prikaz pitanja; bodovanje i rang-lista.
- **Komponente:** WebSocket servis, Redis (stanje igre i rang-lista), API, PostgreSQL, frontend.
- **Što vježbaš:** kratki vršni skokovi prometa (svi odgovaraju u istoj sekundi), load test, stanje igre kad se pod restartira.

### 17. Minimalni webshop

Webshop razbijen u nekoliko malih servisa: katalog, košarica i narudžbe, s lažnim plaćanjem.

- **Minimalno:** katalog proizvoda; košarica po korisniku; narudžba koja poziva mock servis za plaćanje (koji ponekad namjerno ne uspije).
- **Komponente:** 3 mala servisa (katalog, košarica, narudžbe), PostgreSQL, Redis za košaricu, mock plaćanje.
- **Što vježbaš:** više servisa u istom pipelineu i Helm chartu, komunikacija između servisa, distribuirano praćenje (tracing) jednog zahtjeva kroz sve servise.

### 18. Telemetrija senzora

Simulirani senzori temperature i vlage šalju mjerenja svakih nekoliko sekundi; sustav ih sprema i prikazuje na dashboardu.

- **Minimalno:** generator podataka (više lažnih senzora); ingest API; spremanje u time-series bazu; upiti za prosjek i maksimum po senzoru.
- **Komponente:** generator, ingest API, TimescaleDB ili InfluxDB, Grafana.
- **Što vježbaš:** kontinuiran dotok podataka, retencija (brisanje starih podataka), Grafana dashboard nad vlastitim podacima; alert kad senzor prestane slati.

### 19. Praćenje gradskih autobusa

Simulator šalje GPS pozicije nekoliko autobusa po zadanim linijama, a karta prikazuje gdje se trenutno nalaze.

- **Minimalno:** simulator koji pomiče autobuse po ruti; ingest pozicija; zadnja pozicija svakog autobusa u Redisu; karta na frontendu (npr. Leaflet).
- **Komponente:** simulator, ingest API, Redis, PostgreSQL za povijest, frontend s kartom.
- **Što vježbaš:** stream podataka, latencija od pozicije do prikaza kao metrika, skaliranje ingesta.

### 20. Pretraživač dokumenata

Korisnik uploada dokumente (TXT, Markdown, PDF), sustav ih indeksira i omogućuje pretragu po sadržaju.

- **Minimalno:** upload; indekser koji izvuče tekst i pošalje ga u search engine; pretraga s isticanjem pogodaka.
- **Komponente:** upload API, indekser worker, [Meilisearch](https://www.meilisearch.com/) (lakši) ili OpenSearch (teži, traži puno RAM-a), MinIO za originale.
- **Što vježbaš:** stateful servis na Kubernetesu (PersistentVolume), backup i vraćanje indeksa, što se dogodi kad se indeks izgubi.

### 21. Feature-flag servis

Vlastiti mali servis za feature flagove: admin uključuje i isključuje funkcionalnosti, a druge aplikacije pitaju servis je li određena funkcionalnost uključena za određenog korisnika.

- **Minimalno:** CRUD flagova; pravila (uključeno za sve, za X % korisnika, za listu korisnika); brzi `GET` za provjeru s cacheom; mala demo aplikacija koja koristi servis.
- **Komponente:** API, PostgreSQL, Redis cache, admin sučelje, demo klijent.
- **Što vježbaš:** canary i postupno puštanje funkcionalnosti (povezano sa 7. tjednom), latencija kao kritična metrika, što klijent radi kad servis ne radi (fallback).

### 22. RAG chatbot nad FAQ-om

Chatbot koji odgovara na pitanja studenata na temelju skupa dokumenata (FAQ, pravilnici) koristeći lokalni jezični model i vektorsku pretragu.

- **Minimalno:** učitavanje dokumenata i izrada embeddinga; spremanje u vektorsku bazu; endpoint koji za pitanje nađe relevantne dijelove i generira odgovor s izvorom.
- **Komponente:** API, pgvector ili Qdrant, [Ollama](https://ollama.com/) s malim modelom, worker za indeksiranje.
- **Što vježbaš:** resursi i limiti (LLM traži puno memorije i CPU-a), duga trajanja zahtjeva i timeouti, monitoring LLM servisa (povezano s 14. tjednom).
- **Napomena:** traži najmanje 16 GB RAM-a za ugodan rad. Na slabijem računalu koristiti najmanji model ili odabrati drugi projekt.

---

## Vlastiti prijedlog

Može, uz odobrenje nastavnika do kraja 2. tjedna. U prijedlogu navedi:

1. što aplikacija radi (dvije rečenice),
2. koje su 3+ komponente,
3. što je na njoj zanimljivo za infrastrukturu (pozadinski posao, stanje, opterećenje, vanjska ovisnost).

Ako ne možeš odgovoriti na treće pitanje, aplikacija vjerojatno nije dobar izbor za ovaj kolegij.
