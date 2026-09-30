# Praktikum — DevOps i infrastruktura · silabus

Sveučilište Jurja Dobrile u Puli · Fakultet informatike · akademska godina 2026./27.

> Plan vježbi tjedan po tjedan, s poveznicama na kod i materijale, nalazi se u [README-u repozitorija](../README.md#plan-vježbi).

---

## 1. Informacije o kolegiju

| Stavka | Vrijednost |
| --- | --- |
| Kod i naziv kolegija | [kod], Praktikum (DevOps i infrastruktura) |
| Nastavnici | Ratomir Karlović, mag. inf. (predavanja – teorijski dio); Vanja Luk, mag. inf. (vježbe – praktični dio) |
| Studijski program | Informatika (prijediplomski) |
| Vrsta kolegija | obvezni |
| Semestar / godina | zimski (5. semestar) / III. |
| Mjesto izvođenja | Pula, informatički laboratorij, e-učenje |
| Jezik izvođenja | hrvatski, engleski |
| Broj ECTS bodova | 6 |
| Broj sati u semestru | 30P – 30V – 0S (redoviti) |
| Preduvjeti | nema formalnih; preporučeno: Operacijski sustavi, Mrežni sustavi, Programiranje u skriptnim jezicima, Web aplikacije, Baze podataka II |

---

## 2. Cilj kolegija

Cilj kolegija je osposobiti studente da samostalno isporuče i održavaju softver na način na koji se to radi u industriji: od verzioniranog koda preko automatiziranog pipelinea do aplikacije pod monitoringom u produkciji.

Kolegij je praktičan. Svaki termin završava radom u laboratoriju, a sve cjeline grade isti individualni projekt koji do kraja semestra postaje potpuno automatizirani deployment jedne multi-service aplikacije.

Posebna nit kroz kolegij je primjena umjetne inteligencije u radu na infrastrukturi: studenti koriste AI asistente za pisanje skripti, konfiguracija i analizu incidenata, ali uz provjeru, testiranje i svijest o sigurnosnim rizicima. Slijepo korištenje AI-ja nije dopušteno: student mora razumjeti što AI radi u njegovim skriptama i konfiguracijama i moći objasniti svaku liniju koju preda.

---

## 3. Ishodi učenja

Nakon odslušanog kolegija student će moći:

1. Objasniti načela DevOps kulture i vrednovati delivery performance pomoću DORA metrika.
2. Koristiti Linux, Git i skriptiranje za svakodnevne operativne zadatke.
3. Kontejnerizirati multi-service aplikaciju i pokrenuti je na Kubernetes clusteru.
4. Izgraditi CI/CD pipeline koji automatski radi build, test i deploy aplikacije.
5. Primijeniti Infrastructure as Code i configuration management (Terraform/OpenTofu, Ansible).
6. Uspostaviti monitoring, alerting i osnovne security kontrole u pipelineu.
7. Kritički primijeniti AI alate u radu na infrastrukturi i procijeniti njihova ograničenja i rizike.

---

## 4. Sadržaj kolegija

Svaki termin ima dva dijela: 2 sata predavanja (teorijski dio) i 2 sata vježbi u laboratoriju (praktični dio). Vježbe se nadovezuju na predavanje istog dana. Laboratorijski zadaci nadograđuju isti individualni projekt, a „AI kutak“ u svakom terminu pokazuje kako se AI koristi u toj cjelini.

| Tj. | Predavanja (teorija) | Vježbe (praksa) | AI kutak | Ishodi |
| --- | --- | --- | --- | --- |
| 1 | Uvod u DevOps: kultura, CALMS, DORA metrike, uloge (DevOps, SRE, platform engineering) | Prijava za GitHub Education (Student Developer Pack) sa studentskim e-mailom, izrada privatnog repozitorija iz predloška kolegija (`praktikum-project-template`); postavljanje okruženja: instalacija WSL2 + Docker (Windows), `make check` i `make cluster-up`, SSH ključevi | Pravila korištenja AI alata na kolegiju | 1 |
| 2 | Linux za ops: procesi, systemd, logovi, networking, permissions | Bash skripte za automatizaciju, cron, troubleshooting servisa | Generiranje i provjera bash skripti | 2 |
| 3 | Git i suradnja: branching, pull requesti, code review, trunk-based development | Git workflow na vlastitom projektu (branchevi, PR-ovi, branch protection, commit konvencije); review tuđeg PR-a | AI kao code reviewer | 2 |
| 4 | Kontejneri I: Docker, images, layers, registry | Dockerfile za projekt, multi-stage build, push imagea u registry | Optimizacija Dockerfilea uz AI | 3 |
| 5 | Kontejneri II: Docker Compose, networks, volumes, multi-service aplikacije | Aplikacija + baza + cache u Composeu | — | 3 |
| 6 | Continuous Integration (CI): GitHub Actions / GitLab CI | Pipeline: lint, testovi, build imagea | Generiranje workflowa i debugging | 4 |
| 7 | Continuous Delivery (CD): okruženja, artefakti, blue-green, canary, feature flags | Automatski deploy na staging; **kontrolna točka projekta 1** | — | 1, 4 |
| 8 | Infrastructure as Code (IaC): Terraform/OpenTofu, state, moduli | Provisioning VM-a i mreže u cloudu ili lokalno | Pisanje i review IaC-a uz AI | 5 |
| 9 | Configuration management: Ansible, idempotentnost | Ansible playbook za konfiguraciju servera | — | 5 |
| 10 | Kubernetes I: Pods, Deployments, Services, ConfigMaps, Secrets | Deploy projekta na lokalni cluster (kind/k3s) | Objašnjavanje YAML manifesta | 3 |
| 11 | Kubernetes II: Helm, ingress, GitOps (Argo CD) | Helm chart za projekt, GitOps deploy | — | 3, 4 |
| 12 | Observability: metrics, logs, traces, SLI/SLO, alerting | Prometheus + Grafana, dashboard i alert za projekt | AIOps: anomaly detection | 6 |
| 13 | DevSecOps: secrets management, image scanning, SBOM, supply chain security, least privilege | Trivy/secret scanning u pipelineu; **kontrolna točka projekta 2** | Rizici: curenje secreta u promptove, hallucinated paketi (slopsquatting) | 6, 7 |
| 14 | AI u DevOps praksi: AI agenti u terminalu, incident response, postmortem, pregled LLMOps-a | Simulirani incident: troubleshooting uz AI, pisanje postmortema | Cijeli termin | 7 |
| 15 | Završne prezentacije i obrana projekata | Demo pipelinea, pitanja | — | 1–7 |

---

## 5. Planirane aktivnosti, metode učenja i poučavanja i načini vrednovanja

Sav rad je individualan. Ocjena se gradi kontinuirano: projekt nosi polovicu, laboratorijski zadaci trećinu, a usmena obrana provjerava da je student sam razumio i napravio ono što je predao.

| Aktivnost | Ishodi | Sati | ECTS | Udio ocjene |
| --- | --- | --- | --- | --- |
| Predavanja (teorijski dio) | 1–7 | 30 | 1,0 | 0% |
| Vježbe (praktični dio) | 2–7 | 30 | 1,0 | 0% |
| Laboratorijski zadaci (10 predaja) | 2–6 | 30 | 1,0 | 30% |
| Individualni projekt (2 kontrolne točke + završna predaja) | 3–7 | 60 | 2,0 | 50% |
| Završna prezentacija i usmena obrana | 1–7 | 30 | 1,0 | 20% |
| **Ukupno** | 1–7 | 180 | 6,0 | 100% |

**Laboratorijski zadaci.** Svaki lab je jedan pull request s labelom `lab-XX` u studentovom repozitoriju, otvoren do početka sljedećeg termina. Popis zadataka po tjednima, s poveznicama na kod i materijale, nalazi se u [planu vježbi](../README.md#plan-vježbi). Svaki zadatak nosi 3 boda; broji se 10 najboljih od 13 predaja.

**Individualni projekt.** Svaki student odabire vlastitu multi-service aplikaciju ([s popisa kolegija](popis-projekata.md) ili uz odobrenje nastavnika), tako da nema dva ista projekta. Do kraja semestra mora imati: Dockerfile i docker-compose, CI/CD pipeline, Infrastructure as Code, deploy na Kubernetes, dashboard s alertom, security provjere u pipelineu i kratki postmortem simuliranog incidenta. Kontrolne točke su git tagovi `checkpoint-1` (7. tjedan) i `checkpoint-2` (13. tjedan) i nose po 10 bodova, završna predaja 30. Napredak se prati kroz povijest commitova.

**Korištenje AI alata.** AI alati su dopušteni i potaknuti. Uz projekt se predaje kratki AI dnevnik ([`docs/ai-log.md`](ai-log.md)): za što je AI korišten, što je predložio i što je student provjerio ili ispravio. Student mora na obrani objasniti svaki dio koda i konfiguracije.

**Metode:** predavanja (teorijski dio, uz raspravu i primjere iz prakse), vježbe u laboratoriju uz demonstraciju uživo i vođeni rad (praktični dio), samostalni rad na projektu uz version control (GitHub/GitLab, issues), peer code review (student reviewa tuđi PR, ali ne piše tuđi kod), rasprava na forumu kolegija, samostalno istraživanje službene dokumentacije.

**Kriteriji ocjenjivanja** (Pravilnik o ocjenjivanju UNIPU):

| Ocjena | Postignuće |
| --- | --- |
| izvrstan (5) | 89–100% |
| vrlo dobar (4) | 76–88,9% |
| dobar (3) | 63–75,9% |
| dovoljan (2) | 50–62,9% |

---

## 6. Studentske obveze, rokovi i ostalo

Da položi kolegij, student mora:

1. prisustvovati na najmanje 70% termina,
2. ostvariti najmanje 50% bodova iz laboratorijskih zadataka,
3. predati i obraniti projekt s najmanje 50% bodova projekta,
4. ukupno ostvariti najmanje 50 od 100 bodova.

Student koji ne zadovolji uvjete kontinuiranog praćenja predaje doradu projekta i pristupa usmenoj obrani na ispitnom roku.

**Rokovi.** Ispitni rokovi objavljuju se na početku akademske godine u ISVU-u. Rokovi laboratorijskih zadataka i kontrolnih točaka objavljuju se na e-učenju.

**Ostalo.** Materijali, upute za laboratorij i predložak projekta objavljuju se na e-učenju i u repozitoriju kolegija. Za rad je potrebno vlastito računalo s najmanje 8 GB RAM-a ili pristup laboratorijskom računalu; studenti koriste besplatne račune (GitHub Student Developer Pack, lokalni cluster). Predaja tuđeg rješenja ili nedeklarirano kopiranje AI outputa povlači disciplinsku odgovornost. Položeni dijelovi priznaju se do kraja tekuće akademske godine.

---

## 7. Literatura

**Obvezna:**

1. Nastavni materijali, upute za laboratorij i predložak projekta (e-učenje, repozitorij kolegija).
2. Službena dokumentacija: Docker, GitHub Actions, Terraform/OpenTofu, Ansible, Kubernetes, Prometheus.

**Izborna:**

Sva izborna literatura slobodno je i legalno dostupna online.

1. Beyer, B., Jones, C., Petoff, J., Murphy, N. R. (ur.): *Site Reliability Engineering: How Google Runs Production Systems*, O’Reilly, 2016. ISBN 978-1491929124. Dostupno na [sre.google/sre-book](https://sre.google/sre-book/table-of-contents/).
2. Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K., Thorne, S. (ur.): *The Site Reliability Workbook: Practical Ways to Implement SRE*, O’Reilly, 2018. ISBN 978-1492029502. Dostupno na [sre.google/workbook](https://sre.google/workbook/table-of-contents/).
3. Adkins, H., Beyer, B., Blankinship, P., Lewandowski, P., Oprea, A., Stubblefield, A.: *Building Secure and Reliable Systems: Best Practices for Designing, Implementing, and Maintaining Systems*, O’Reilly, 2020. ISBN 978-1492083122. Dostupno na [sre.google/books](https://sre.google/books/).
4. Chacon, S., Straub, B.: *Pro Git*, 2nd ed., Apress, 2014. ISBN 978-1484200773. Dostupno na [git-scm.com/book](https://git-scm.com/book/en/v2) (licenca CC BY-NC-SA 3.0, PDF i EPUB).
5. Shotts, W.: *The Linux Command Line*, No Starch Press, 2019. ISBN 978-1593279523. Dostupno na [linuxcommand.org](https://linuxcommand.org/tlcl.php) (licenca CC BY-NC-ND 3.0, PDF).

---

## 8. Načini praćenja kvalitete

Laboratorijski zadaci, kontrolne točke projekta, završna prezentacija i usmena obrana; anonimna studentska anketa sredinom i na kraju semestra; analiza AI dnevnika radi dorade uputa za sljedeću godinu.
