# Što se od tebe očekuje

Ovaj dokument odgovara na većinu pitanja koja se pojave tijekom semestra. **Pročitaj ga cijelog prije prvog termina** i vrati mu se prije nego što pošalješ pitanje — velika je vjerojatnost da je odgovor ovdje.

---

## Ukratko

- Cijeli semestar radiš **jedan individualni projekt** u **svom privatnom GitHub repozitoriju** napravljenom iz predloška kolegija.
- Svaki tjedan od 2. do 14. predaješ **jedan lab zadatak** kao **pull request** s labelom `lab-XX`, do početka sljedećeg termina.
- U 7. i 13. tjednu staviš git tag **`checkpoint-1`** odnosno **`checkpoint-2`**. U 15. tjednu je **završna predaja i obrana**.
- **Ocjenjuje se infrastruktura, ne aplikacija.** Aplikacija smije biti jednostavna i generirana uz AI.
- **AI alati su dopušteni**, ali svako značajnije korištenje zapisuješ u `docs/ai-log.md`, a na obrani moraš objasniti svaku liniju koju si predao.
- Sav rad je **individualan**.

---

## 1. Bodovanje i uvjeti za prolaz

| Što | Kada | Bodovi |
| --- | --- | --- |
| Laboratorijski zadaci (10 najboljih od 13, po 3 boda) | 2.–14. tjedan | 30 |
| Checkpoint 1 | 7. tjedan | 10 |
| Checkpoint 2 | 13. tjedan | 10 |
| Završna predaja projekta | 15. tjedan | 30 |
| Završna prezentacija i usmena obrana | 15. tjedan | 20 |
| **Ukupno** | | **100** |

**Da položiš kroz semestar, moraš:**

1. prisustvovati na najmanje **70 % termina** (najviše 4 izostanka od 15),
2. skupiti najmanje **15 od 30** bodova iz labova,
3. skupiti najmanje **25 od 50** bodova iz projekta (checkpointi + završna predaja) i obraniti ga,
4. skupiti ukupno najmanje **50 od 100** bodova.

| Ocjena | Bodovi |
| --- | --- |
| izvrstan (5) | 89–100 |
| vrlo dobar (4) | 76–88,9 |
| dobar (3) | 63–75,9 |
| dovoljan (2) | 50–62,9 |

Ako ne zadovoljiš uvjete, na ispitnom roku predaješ doradu projekta i pristupaš usmenoj obrani. Detalji su u [silabusu](silabus.md).

---

## 2. Tvoj repozitorij

U 1. tjednu:

1. Na GitHubu otvori predložak **`praktikum-project-template`** i klikni **Use this template → Create a new repository**.
2. Ime repozitorija: **`praktikum-<prezime>`** (malim slovima, bez dijakritika, npr. `praktikum-horvat`).
3. Vidljivost: **Private**.
4. Settings → Collaborators → dodaj nastavnika (GitHub username dobit ćeš na prvom terminu).
5. Poveznicu na repozitorij predaj na e-učenju.
6. U `README.md` ispuni sekciju **Moj projekt**.

**Jedan repozitorij za cijeli semestar.** Ne radi novi repo za svaki lab.

Ovaj repozitorij (`praktikum-demo-app`) je **ogledna aplikacija s vježbi** — tu gledaš primjere i materijale, ali ovdje **ništa ne predaješ**.

---

## 3. Kako predati lab

Svaki lab ide istim postupkom:

```bash
git switch main && git pull
git switch -c lab-06-ci            # nova grana za lab
# ... radiš ...
git add -A
git commit -m "ci: add docker build job"
git push -u origin lab-06-ci
```

Zatim na GitHubu:

1. Otvori **pull request** prema `main`.
2. Dodaj labelu **`lab-06`** (broj tjedna). Ako labela ne postoji, napravi je: Issues → Labels → New label.
3. Ispuni **PR template** — kako si provjerio da radi i jesi li koristio AI.
4. Pričekaj da **CI bude zelen** (od 6. tjedna).
5. Kad je sve u redu, **mergeaj sam**. Ne čekaj odobrenje nastavnika za merge.

**Rok je početak sljedećeg termina.** Računa se trenutak **otvaranja** pull requesta, ne mergea. Ocjenjuje se stanje u trenutku roka — commitovi nakon roka ne mijenjaju bodove za taj lab.

**Zakašnjeli lab ne nosi bodove**, ali ga svejedno napravi i mergeaj: sljedeći labovi grade na njemu. Zato se broji 10 najboljih od 13 — tri lošija ili propuštena laba ne ruše ocjenu.

### Kako se boduje lab

Svaki lab ima svoje kriterije prihvaćanja u lekciji tog tjedna (npr. [`docs/week-02-healthcheck.md`](week-02-healthcheck.md)). Općenito:

| Bodovi | Značenje |
| --- | --- |
| 3 | ispunjeni svi kriteriji prihvaćanja |
| 2 | radi, ali nedostaje jedna stavka |
| 1 | radi samo djelomično ili samo u "sretnom slučaju" |
| 0 | ne radi, nije predano na vrijeme ili nije tvoj rad |

---

## 4. Projekt

### Odabir aplikacije

- Biraš s [popisa projekata](popis-projekata.md) ili predlažeš vlastitu uz odobrenje.
- **Tko prvi prijavi, taj dobije.** Dvoje studenata ne može imati istu aplikaciju.
- **Rok za odabir i prijavu: kraj 2. tjedna.** Vlastiti prijedlog mora biti odobren do tog roka.
- Minimum: **API + baza + Redis**, `/health` koji provjerava obje veze, nekoliko testova.
- **Odaberi jednostavno.** Svaka dodatna komponenta znači još jedan Dockerfile, još jedan servis u composeu, još jedan Deployment i još jednu stvar koja može puknuti u 10. tjednu.

### Checkpointi

Checkpoint je **snimka stanja tvog repozitorija** u trenutku roka. Kad misliš da si spreman:

```bash
git switch main && git pull
git tag checkpoint-1
git push origin checkpoint-1
```

Ocjenjuje se ono što je na tagu. Što se ocjenjuje piše u **checklisti u `README.md` tvog repozitorija**. Ako tag postaviš prerano pa nešto popraviš, možeš ga pomaknuti prije roka:

```bash
git tag -f checkpoint-1
git push -f origin checkpoint-1
```

Nakon roka tag se ne pomiče.

### Završna predaja

Rok je dan prije obrana (točan datum na e-učenju). Na `main` grani mora biti:

- sve stavke iz checkliste u `README.md`,
- `README.md` koji objašnjava kako pokrenuti projekt od nule — netko drugi mora to moći ponoviti,
- `docs/postmortem.md` (14. tjedan),
- `docs/ai-log.md` vođen kroz semestar.

---

## 5. Obrana

Traje oko **15 minuta**:

| | Što |
| --- | --- |
| ~5 min | **Demo:** mala promjena u kodu → PR → CI zelen → merge → image u GHCR-u → Argo CD sync → promjena vidljiva u aplikaciji |
| ~6 min | **Pitanja o tvom kodu:** nastavnik otvori datoteku i pita "što radi ovaj red i zašto je tu?" |
| ~4 min | **Pitanja iz AI loga:** "što je AI predložio, što si promijenio, kako si provjerio?" |

**Dođi s dignutim clusterom i Argo CD-om koji radi.** Ako se nešto sruši tijekom demoa, to je prilika da pokažeš troubleshooting, a ne kazna.

**Pravilo: dio koda ili konfiguracije koji ne znaš objasniti ne nosi bodove** — bez obzira na to radi li.

---

## 6. AI alati

**Smiješ** koristiti bilo koji AI alat (ChatGPT, Claude, Copilot, Cursor…) za bilo koji dio projekta.

**Moraš:**

- za svako značajnije korištenje dopisati zapis u `docs/ai-log.md` (predložak je u datoteci),
- označiti kvačicu u PR templateu,
- razumjeti i moći objasniti sve što predaš.

**Što je "značajnije korištenje"?** Kad je AI napisao ili bitno promijenio kod, konfiguraciju ili dijagnozu problema. Pitanje "što znači ova greška" koje ti je pomoglo da sam nađeš rješenje ne treba zapisivati.

**Nedeklarirano korištenje** — kod koji je napisao AI, a nije u AI logu — tretira se kao predaja tuđeg rješenja.

**Nikad ne lijepi u AI:** lozinke, tokene, `.env` datoteke ili logove u kojima se vide secreti. Prije lijepljenja outputa provjeri što je u njemu.

AI log se **ne ocjenjuje po tome koliko si AI koristio**, nego po tome koliko si kritičan: što je predložio, što nije radilo, što si provjerio i ispravio.

---

## 7. Računalo i okruženje

- **Minimalno 8 GB RAM-a**, preporučeno 16 GB. U 11. i 12. tjednu na tvom računalu istovremeno rade Kubernetes, Argo CD, Prometheus i tvoja aplikacija.
- **Windows:** sve radiš unutar **WSL2** (Ubuntu). Docker Desktop mora imati uključenu WSL integraciju. **Repozitorij kloniraj u Linux home (`~/`), ne u `/mnt/c/...`** — inače je sve višestruko sporije.
- **macOS i Linux** rade bez posebnih koraka.
- Upute za instalaciju stižu tjedan prije prve nastave. **Instaliraj sve prije prvog termina** — WSL traži admin prava i restart.
- Ako tvoje računalo ne može, javi se **u 1. tjednu**; možeš raditi na laboratorijskom računalu.
- **Ne treba ti cloud račun ni kartica.** Sve radi lokalno.

---

## 8. Kako postaviti pitanje

Pitanja postavljaj na **forumu kolegija na e-učenju**, ne privatnim porukama — odgovor će pomoći i drugima. Za osobne stvari (izostanci, zdravlje, dogovori) piši nastavniku mailom.

**Prije nego što pitaš:**

1. Pročitaj **ovaj dokument**, **lekciju tog tjedna** u `docs/` i **README mape** s kojom radiš.
2. Pogledaj **stanje ogledne aplikacije** za taj tjedan: `git checkout week-XX` u ovom repozitoriju.
3. Pročitaj **cijelu poruku greške**, ne samo zadnji red. Pola odgovora je u njoj.
4. Provjeri **tablicu čestih problema** u README-u mape (npr. [`kind/README.md`](../kind/README.md)).
5. Potraži grešku na webu ili pitaj AI — i zapiši to u AI log ako ti je pomoglo.

**Kad pitaš, napiši:**

- **Što pokušavaš napraviti** (koji lab, koji korak)
- **Što očekuješ da se dogodi**
- **Što se stvarno dogodi** — cijela poruka greške kao tekst, ne screenshot mobitelom
- **Što si već probao**
- **Poveznica na commit ili PR** ako je relevantno

Pitanje "ne radi mi Docker" ne može dobiti odgovor. Pitanje s ovih pet stavki obično dobije odgovor u nekoliko minuta — a često ga nađeš sam dok ga pišeš.

---

## 9. Česta pitanja

**Moram li pisati u Pythonu?**
Ne. Jezik i framework biraš sam. Ako ne koristiš Python, prilagodi `Makefile` i CI workflow — to je dio zadatka.

**Moram li imati frontend?**
Ne, osim ako to ne piše u opisu aplikacije. API koji se može isprobati `curl`-om ili kroz `/docs` je dovoljan.

**Mogu li koristiti GitLab umjesto GitHuba?**
Ne. Materijali, predložak i CI su za GitHub i GitHub Actions.

**Mogu li koristiti AWS, Azure ili GCP umjesto lokalnog clustera?**
Za učenje možeš, ali predaja i obrana moraju raditi lokalno (kind), jer tako se ocjenjuje. Ne treba ti cloud i ne preporučuje se.

**Smijem li raditi s kolegom?**
Možete razgovarati o konceptima i pomagati si s greškama. Kod i konfiguraciju pišeš sam. Isti Dockerfile, pipeline ili Helm chart kod dvoje studenata tretira se kao plagijat.

**Mogu li promijeniti aplikaciju usred semestra?**
Do kraja 3. tjedna uz javljanje nastavniku, ako nova aplikacija nije zauzeta. Poslije toga ne.

**Što ako mi kod aplikacije stvarno ne ide?**
Javi se do kraja 2. tjedna i dobit ćeš gotovu jednostavnu aplikaciju; cijeli semestar radiš samo infrastrukturu oko nje. Bodovi se ne mijenjaju.

**Propustio sam termin. Što sad?**
Pogledaj lekciju u `docs/` i stanje ogledne aplikacije (`git checkout week-XX`, `git diff week-XX week-YY`). Lab predaješ u istom roku kao svi. Izostanak se računa u 30 % dopuštenih.

**Mogu li popraviti lab nakon roka da dobijem više bodova?**
Ne. Popravi ga svakako, jer sljedeći labovi grade na njemu, ali bodovi ostaju prema stanju u roku. Za to postoji pravilo 10 od 13.

**Mogu li sam mergeati svoj pull request?**
Da, i trebaš. Kod branch protectiona postavi **broj obaveznih odobrenja (required approvals) na 0** — radiš sam, pa ne možeš sam sebi odobriti PR. Obavezni ostaju pull request i zeleni CI.

**CI mi je crven zbog nečega što nije moj lab. Mogu li predati?**
Predaj PR u roku, u opisu napiši što ne radi i zašto. Bolje je predati s objašnjenjem nego ne predati.

**Commitao sam lozinku ili token. Što da radim?**
1. **Odmah opozovi ili promijeni** taj secret — ovo je jedini korak koji stvarno pomaže.
2. Makni ga iz koda i stavi u `.env` ili GitHub Secrets.
3. Javi se nastavniku; zajedno ćemo vidjeti treba li ga maknuti i iz povijesti gita.
Brisanje u sljedećem commitu **nije dovoljno** — secret ostaje u povijesti.

**Koliko vremena tjedno trebam?**
Kolegij nosi 6 ECTS, što je oko 180 sati ukupno. Nakon 60 sati nastave ostaje oko **8 sati tjedno** samostalnog rada. Ako ti treba znatno više, javi se — vjerojatno je aplikacija prevelika ili negdje zapinješ.

**Moj repozitorij je slučajno javan. Je li to problem?**
Prebaci ga na privatan (Settings → General → Danger Zone → Change visibility) i provjeri da u povijesti nema secreta. Image u GHCR-u može biti javan — to je u redu i olakšava rad u 10. i 11. tjednu.

**Zašto se ne ocjenjuje aplikacija?**
Jer kolegij uči kako se softver isporučuje i održava, a ne kako se piše. Na poslu ćeš jednako često dobiti tuđu aplikaciju koju treba deployati kao što ćeš pisati svoju.
