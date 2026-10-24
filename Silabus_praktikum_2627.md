# Praktikum — silabus za IPN 2026./27.

Sep 30, 2026 · @Vanja Luk

Silabus kolegija Praktikum u strukturi izvedbenog plana nastave Fakulteta informatike u Puli, za prijediplomski studij Informatika, 5. semestar. Polja u uglatim zagradama dopunjuje nositelj kolegija.

## 1. Kod i naziv kolegija: \[kod\], Praktikum (\[kratica\])

### Nastavnici

- Ratomir Karlović, mag. inf.
- Vanja Luk, mag. inf.

### Informacije o kolegiju

|  |  |
| --- | --- |
| Studijski program | Informatika (prijediplomski) |
| Vrsta kolegija | obvezni |
| Razina kolegija | prijediplomski |
| Semestar | zimski (5. semestar) |
| Godina studija | III. |
| Mjesto izvođenja | Pula, informatički laboratorij, e-učenje |
| Jezik izvođenja | hrvatski, engleski |
| Broj ECTS bodova | 6 |
| Broj sati u semestru | 0P – 0V – 60S (redoviti) |
| Korelativnost | - |
| Preduvjeti | Nema formalnih preduvjeta za upis kolegija. Preporučeno predznanje: Operacijski sustavi, Mrežni sustavi, Programiranje u skriptnim jezicima, Web aplikacije. |

## 2. Cilj kolegija

Cilj kolegija je osposobiti studente da samostalno isporuče i održavaju softver na način na koji se to radi u industriji: od verzioniranog koda preko automatiziranog pipelinea do aplikacije pod monitoringom. Kolegij je praktičan: svaki termin sastoji se od predavanja i vježbi na istu temu, a sve cjeline grade isti individualni projekt koji do kraja semestra postaje potpuno automatizirani deployment jedne multi-service aplikacije na Kubernetes. Posebna nit kroz kolegij je kritička primjena alata umjetne inteligencije u radu na infrastrukturi, uz provjeru, testiranje i svijest o sigurnosnim rizicima.

## 3. Ishodi učenja

1. Objasniti načela DevOps kulture i vrednovati učinkovitost isporuke softvera pomoću DORA metrika.
2. Koristiti Linux, Git i skriptiranje za svakodnevne operativne zadatke.
3. Kontejnerizirati multi-service aplikaciju i pokrenuti je na Kubernetes clusteru.
4. Izgraditi CI/CD pipeline koji automatski radi build, testiranje i deployment aplikacije.
5. Primijeniti Infrastructure as Code i configuration management.
6. Uspostaviti monitoring, alerting i osnovne sigurnosne kontrole u pipelineu.
7. Kritički primijeniti AI alate u radu na infrastrukturi i procijeniti njihova ograničenja i rizike.

## 4. Sadržaj kolegija

### Predavanja

1. Uvod u DevOps. Kultura i načela (CALMS). DORA metrike. Uloge: DevOps, SRE, platform engineering.
2. Linux za operacije. Procesi i signali, systemd i servisi, logovi, mreža, dozvole. Exit code. Zakazani poslovi.
3. Git i suradnja. Grananje, pull request, code review, trunk-based development, zaštita glavne grane.
4. Kontejneri I. Kontejner i virtualni stroj, image i slojevi, Dockerfile, build cache, multi-stage build, registry.
5. Kontejneri II. Multi-service aplikacije, Docker Compose, mreže, volumeni, konfiguracija kroz okruženje.
6. Continuous Integration. Pipeline, faze i automatske provjere, GitHub Actions.
7. Continuous Delivery. Deployment pipeline, okruženja, verzioniranje artefakata, strategije izdavanja (rolling, blue-green, canary), feature flags.
8. Infrastructure as Code. Deklarativni i imperativni pristup, idempotentnost, stanje i drift, alati (Terraform/OpenTofu).
9. Configuration management. Ansible: inventory, playbook, moduli, handleri, idempotentnost.
10. Kubernetes I. Arhitektura clustera, deklarativni model, Pod, Deployment, Service, ConfigMap, Secret, probe, resursi.
11. Kubernetes II. Helm, ingress, GitOps i Argo CD.
12. Observability. Metrike, logovi i tragovi; četiri zlatna signala; Prometheus i Grafana; SLI, SLO i error budget; alerting.
13. DevSecOps. Upravljanje tajnama, skeniranje imagea, SBOM, sigurnost lanca opskrbe, najmanje ovlasti.
14. AI u DevOps praksi. Upravljanje incidentima, blameless postmortem, AI agenti i AIOps, rizici i ograničenja AI alata, pregled LLMOps-a.
15. Završne prezentacije i obrana projekata.

### Vježbe

1. Postavljanje radnog okruženja (WSL2, Docker, kind, kubectl, Helm, Ansible), izrada osobnog repozitorija iz predloška kolegija.
2. Bash skripta za provjeru dostupnosti servisa, zakazivanje kroz cron, troubleshooting servisa.
3. Rad s granama i pull requestovima na vlastitom projektu, code review, zaštita glavne grane.
4. Dockerfile za vlastitu aplikaciju: multi-stage build, pokretanje bez root ovlasti.
5. Docker Compose za cijeli stack aplikacije (aplikacija, baza, cache).
6. CI pipeline: lint, testovi i build imagea na svaki pull request.
7. Objava imagea u registry nakon mergea u glavnu granu; prva kontrolna točka projekta.
8. Infrastructure as Code za lokalno okruženje.
9. Ansible playbook za pripremu okruženja i pokretanje aplikacije.
10. Deployment aplikacije na lokalni Kubernetes cluster, debugging podova.
11. Helm chart za aplikaciju, GitOps deployment s Argo CD-om.
12. Metrike aplikacije, Prometheus, Grafana dashboard i alert, definicija SLO-a.
13. Skeniranje imagea i tajni u pipelineu; druga kontrolna točka projekta.
14. Simulirani incident, troubleshooting uz AI alate, pisanje postmortema.
15. Završne prezentacije i obrana projekata.

Vježbe se održavaju u istom terminu kao predavanje na istu temu i nadograđuju isti individualni projekt.

## 5. Planirane aktivnosti, metode učenja i poučavanja i načini vrednovanja

### Redoviti studij

| Aktivnost | Ishodi | Sati | ECTS | Udio ocjene |
| --- | --- | --- | --- | --- |
| Predavanja | 1–7 | 30 | 1,0 | 0% |
| Vježbe | 2–7 | 30 | 1,0 | 0% |
| Laboratorijski zadaci | 2–6 | 30 | 1,0 | 30% |
| Individualni projekt | 3–7 | 60 | 2,0 | 50% |
| Završna prezentacija i usmena obrana | 1–7 | 30 | 1,0 | 20% |
| **Ukupno** | 1–7 | 180 | 6,0 | 100% |

U kontinuiranom praćenju broj bodova odgovara udjelu ocjene (ukupno 100 bodova).

### Predavanja

Obrađuju se sve teme navedene u sadržaju kolegija. Predavanje prethodi vježbama u istom terminu i daje teorijsku osnovu za praktični rad. Od studenata se očekuje aktivno sudjelovanje odgovaranjem na pitanja i u raspravi.

Metode učenja i poučavanja:

- Stjecanje znanja: slušanje predavanja, proučavanje literature i službene dokumentacije alata
- Rasprava: rasprava o nastavnim temama na satu i na forumu kolegija

### Vježbe

Na vježbama nastavnik uživo demonstrira primjenu obrađene teme na oglednoj aplikaciji, a studenti isti postupak primjenjuju na svom projektu uz vođenje nastavnika. Stanje ogledne aplikacije nakon svake vježbe dostupno je u repozitoriju kolegija.

Metode učenja i poučavanja:

- Stjecanje znanja: demonstracija uživo, materijali uz vježbe u repozitoriju kolegija
- Praktičan rad: vođeni rad na vlastitom projektu u informatičkom laboratoriju

### Laboratorijski zadaci

Nakon svake vježbe od 2. do 14. tjedna student samostalno izrađuje zadatak na svom projektu i predaje ga kao pull request u osobnom repozitoriju do početka sljedećeg termina. Zadatak se smatra predanim u trenutku otvaranja pull requesta. Svaki zadatak nosi najviše 3 boda; od 13 zadataka boduje se 10 najboljih (najviše 30 bodova).

Metode učenja i poučavanja:

- Implementacija stečenog znanja: samostalno rješavanje zadataka na vlastitom projektu
- Suradnja: code review pull requesta drugog studenta
- Istraživanje: službena dokumentacija alata, online priručnici

### Individualni projekt

Svaki student odabire vlastitu aplikaciju s popisa kolegija ili uz odobrenje nastavnika, tako da dva studenta nemaju isti projekt. Aplikacija se sastoji od najmanje tri komponente (aplikacija, baza podataka i cache). Ocjenjuje se infrastruktura oko aplikacije, a ne sama aplikacija. Do kraja semestra projekt mora sadržavati: Dockerfile i Docker Compose, CI/CD pipeline, Infrastructure as Code, deployment na Kubernetes, dashboard s alertom, sigurnosne provjere u pipelineu i postmortem simuliranog incidenta.

Napredak se prati kroz povijest commitova. Projekt se ocjenjuje kroz dvije kontrolne točke, označene git tagovima u osobnom repozitoriju, i završnu predaju:

| Provjera | Rok | Bodovi |
| --- | --- | --- |
| Kontrolna točka 1 | 7. tjedan | 10 |
| Kontrolna točka 2 | 13. tjedan | 10 |
| Završna predaja | 15. tjedan | 30 |

Metode učenja i poučavanja:

- Praktičan rad: projektni rad u osobnom repozitoriju (GitHub)
- Istraživanje: službena dokumentacija, tehnički priručnici, literatura
- Implementacija stečenog znanja: izrada i dokumentiranje infrastrukture projekta

### Završna prezentacija i usmena obrana

Student uživo demonstrira put promjene od commita do deploymenta i odgovara na pitanja o vlastitom kodu, konfiguraciji i korištenju AI alata. Dio koda ili konfiguracije koji student ne zna objasniti ne nosi bodove.

### Korištenje alata umjetne inteligencije

AI alati su dopušteni. Student uz projekt vodi AI dnevnik u kojem za svako značajnije korištenje navodi što je AI predložio i što je student provjerio ili ispravio. Nedeklarirano korištenje AI alata smatra se korištenjem tuđeg rješenja.

### Kriteriji ocjenjivanja

Prema Pravilniku o ocjenjivanju UNIPU:

| Ocjena | Postignuće |
| --- | --- |
| izvrstan (5) | 89–100% |
| vrlo dobar (4) | 76–88,9% |
| dobar (3) | 63–75,9% |
| dovoljan (2) | 50–62,9% |

## 6. Studentske obveze

Student može položiti kolegij putem kontinuiranog praćenja tijekom semestra ili na ispitnom roku.

Da položi kolegij putem kontinuiranog praćenja, student mora:

1. ostvariti najmanje 50% bodova iz laboratorijskih zadataka,
2. predati i obraniti projekt s najmanje 50% bodova projekta,
3. ukupno ostvariti najmanje 50 od 100 bodova.

Prisutnost na predavanjima i vježbama nije obavezna i ne utječe na prolaznost. Preporučuje se ipak dolaziti: na vježbama se uživo radi ono što se taj tjedan predaje kao laboratorijski zadatak.

Student koji ne zadovolji uvjete kontinuiranog praćenja predaje doradu projekta i pristupa usmenoj obrani na ispitnom roku.

Studenti su obvezni:

- prijaviti se na mrežne stranice kolegija na sustavu za e-učenje i pratiti obavijesti,
- izraditi osobni privatni repozitorij iz predloška kolegija i omogućiti pristup nastavniku.

## 7. Rokovi ispita i kolokvija

Ispitni rokovi objavljuju se na početku akademske godine na mrežnim stranicama Fakulteta informatike i u ISVU. Rokovi laboratorijskih zadataka i kontrolnih točaka projekta objavljuju se na sustavu za e-učenje.

## 8. Ostale važne činjenice vezane uz kolegij

Tjedni raspored nastavnih aktivnosti objavljuje se početkom semestra. Materijali za učenje, upute za vježbe i predložak projekta objavljuju se na sustavu za e-učenje i u repozitoriju kolegija. Za rad je potrebno vlastito računalo s najmanje 8 GB RAM-a ili pristup laboratorijskom računalu; koriste se besplatni alati i lokalni Kubernetes cluster, bez potrebe za plaćenim cloud uslugama.

Sav rad na kolegiju je individualan. Predaja tuđeg rješenja ili nedeklarirano kopiranje sadržaja generiranog AI alatima povlači disciplinsku odgovornost. Položeni dijelovi kontinuiranog praćenja priznaju se do isteka tekuće akademske godine.

## 9. Literatura

**Obvezna:**

1. Nastavni materijali, upute za vježbe i predložak projekta (sustav za e-učenje, repozitorij kolegija).
2. Službena dokumentacija alata: Docker, GitHub Actions, Terraform/OpenTofu, Ansible, Kubernetes, Helm, Argo CD, Prometheus.

**Izborna:**

Sva izborna literatura slobodno je i legalno dostupna online.

1. Beyer, B., Jones, C., Petoff, J., Murphy, N. R. (ur.): Site Reliability Engineering: How Google Runs Production Systems, O’Reilly, 2016. ISBN 978-1491929124. Dostupno na [sre.google/sre-book](https://sre.google/sre-book/table-of-contents/).
2. Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K., Thorne, S. (ur.): The Site Reliability Workbook: Practical Ways to Implement SRE, O’Reilly, 2018. ISBN 978-1492029502. Dostupno na [sre.google/workbook](https://sre.google/workbook/table-of-contents/).
3. Adkins, H., Beyer, B., Blankinship, P., Lewandowski, P., Oprea, A., Stubblefield, A.: Building Secure and Reliable Systems: Best Practices for Designing, Implementing, and Maintaining Systems, O’Reilly, 2020. ISBN 978-1492083122. Dostupno na [sre.google/books](https://sre.google/books/).
4. Chacon, S., Straub, B.: Pro Git, 2nd ed., Apress, 2014. ISBN 978-1484200773. Dostupno na [git-scm.com/book](https://git-scm.com/book/en/v2) (licenca CC BY-NC-SA 3.0, PDF i EPUB).
5. Shotts, W.: The Linux Command Line, No Starch Press, 2019. ISBN 978-1593279523. Dostupno na [linuxcommand.org](https://linuxcommand.org/tlcl.php) (licenca CC BY-NC-ND 3.0, PDF).

## 10. Načini praćenja kvalitete koji osiguravaju stjecanje izlaznih znanja, vještina i kompetencija

Laboratorijski zadaci, kontrolne točke projekta, završna prezentacija i usmena obrana, anonimna studentska anketa sredinom i na kraju semestra.
