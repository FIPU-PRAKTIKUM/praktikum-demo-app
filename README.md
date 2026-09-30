# Praktikum — ogledna aplikacija (demo-app)

Ovo je aplikacija koju nastavnik gradi uživo na vježbama. Svaki tjedan dobiva novi sloj infrastrukture — isti koji ti taj tjedan dodaješ na svoju aplikaciju u vlastitom repozitoriju.

Aplikacija je **URL shortener** (API + PostgreSQL + Redis) i zato nije na popisu aplikacija za studente. Do 3. tjedna ovdje je placeholder API iz predloška.

**Silabus kolegija:** [`docs/silabus.md`](docs/silabus.md) — ciljevi, ishodi učenja, bodovanje i uvjeti za prolaz.

**Popis projekata:** [`docs/popis-projekata.md`](docs/popis-projekata.md) — aplikacije koje možeš odabrati za svoj projekt.

---

## Kako koristiti ovaj repo

Nakon svake vježbe stanje repozitorija označeno je git tagom `week-XX`. Ako si izostao ili zapeo, pogledaj točno ono što smo napravili na satu:

```bash
git clone <url-ovog-repozitorija>
cd praktikum-demo-app
git checkout week-02            # stanje nakon 2. tjedna
git diff week-01 week-02        # što je točno dodano taj tjedan
git checkout main               # povratak na najnovije stanje
```

Svaka mapa ima svoj `README.md`: što je u njoj, zašto postoji i objašnjenje koda linija po liniju. Lekcije uz vježbe su u [`docs/`](docs/).

**Ovdje se ništa ne predaje.** Domaću zadaću radiš u svom repozitoriju napravljenom iz predloška `praktikum-project-template`, kao pull request s labelom `lab-XX`.

---

## Plan vježbi

| Tj. | Tema | Gdje u repou | Lab | Tag | Stanje |
| --- | --- | --- | --- | --- | --- |
| 1 | [Uvod u DevOps](#1-tjedan--uvod-u-devops) | [`kind/`](kind/), [`scripts/`](scripts/) | setup | `week-01` | gotovo |
| 2 | [Linux za ops](#2-tjedan--linux-za-ops) | [`scripts/`](scripts/) | `lab-02` | `week-02` | gotovo |
| 3 | [Git i suradnja](#3-tjedan--git-i-suradnja) | [`app/`](app/) | `lab-03` | `week-03` | planirano |
| 4 | [Kontejneri I](#4-tjedan--kontejneri-i) | [`app/`](app/) | `lab-04` | `week-04` | planirano |
| 5 | [Kontejneri II](#5-tjedan--kontejneri-ii) | root (`compose.yaml`) | `lab-05` | `week-05` | planirano |
| 6 | [Continuous Integration](#6-tjedan--continuous-integration) | [`.github/workflows/`](.github/workflows/) | `lab-06` | `week-06` | planirano |
| 7 | [Continuous Delivery](#7-tjedan--continuous-delivery) | [`.github/workflows/`](.github/workflows/) | `lab-07` | `week-07` | planirano |
| 8 | [Infrastructure as Code](#8-tjedan--infrastructure-as-code) | `infra/` | `lab-08` | `week-08` | otvoreno |
| 9 | [Configuration management](#9-tjedan--configuration-management) | [`infra/ansible/`](infra/ansible/) | `lab-09` | `week-09` | planirano |
| 10 | [Kubernetes I](#10-tjedan--kubernetes-i) | [`k8s/`](k8s/) | `lab-10` | `week-10` | planirano |
| 11 | [Kubernetes II](#11-tjedan--kubernetes-ii) | [`helm/`](helm/), [`argocd/`](argocd/) | `lab-11` | `week-11` | planirano |
| 12 | [Observability](#12-tjedan--observability) | [`monitoring/`](monitoring/), [`app/`](app/) | `lab-12` | `week-12` | planirano |
| 13 | [DevSecOps](#13-tjedan--devsecops) | [`.github/workflows/`](.github/workflows/) | `lab-13` | `week-13` | planirano |
| 14 | [AI u DevOps praksi](#14-tjedan--ai-u-devops-praksi) | [`docs/`](docs/) | `lab-14` | `week-14` | planirano |
| 15 | [Obrane](#15-tjedan--obrane) | cijeli repo | obrana | `final` | planirano |

Checkpointi: tag `checkpoint-1` u 7. tjednu i `checkpoint-2` u 13. tjednu stavljaš na **svoj** repo.

---

### 1. tjedan — Uvod u DevOps

- **Na vježbama:** instalacija WSL2 i alata, repo iz predloška, `make check`, `make cluster-up`; pregled kako će demo-app izgledati na kraju semestra.
- **Kod:** [`kind/`](kind/) — konfiguracija lokalnog clustera objašnjena linija po liniju; [`scripts/check-env.sh`](scripts/check-env.sh) — provjera alata; [`Makefile`](Makefile) — naredbe koje koristimo cijeli semestar.
- **Zadatak:** setup checklist (ne boduje se, ali bez njega ne možeš predati nijedan lab).

### 2. tjedan — Linux za ops

- **Na vježbama:** bash skripta koja provjerava `/health` svih servisa i javlja grešku; cron; troubleshooting servisa kroz logove.
- **Kod:** [`scripts/healthcheck.sh`](scripts/healthcheck.sh) · objašnjenje linija po liniju u [`scripts/README.md`](scripts/README.md).
- **Lekcija:** [`docs/week-02-healthcheck.md`](docs/week-02-healthcheck.md).
- **Zadatak `lab-02`:** vlastita bash skripta za automatizaciju u `scripts/` svog repozitorija.

### 3. tjedan — Git i suradnja

- **Na vježbama:** placeholder API zamijenim URL shortenerom preko grane i pull requesta; pokažem code review i uključim branch protection na `main`.
- **Kod:** [`app/`](app/) — shortener API + PostgreSQL + Redis, s testovima.
- **Zadatak `lab-03`:** vlastita aplikacija s najmanje 3 komponente, `/health` na svakom servisu, testovi, branch protection.

### 4. tjedan — Kontejneri I

- **Na vježbama:** Dockerfile za API — prvo naivni, pa multi-stage i non-root; usporedba veličine imagea.
- **Kod:** `app/Dockerfile` (dodaje se u [`app/`](app/)).
- **Zadatak `lab-04`:** Dockerfile s imageom manjim od 300 MB koji ne radi kao root.

### 5. tjedan — Kontejneri II

- **Na vježbama:** `compose.yaml` za cijeli stack — healthcheck, `depends_on`, volumeni, `.env`. Skripta iz 2. tjedna dobiva nove servise.
- **Kod:** `compose.yaml` u rootu, [`.env.example`](.env.example), [`scripts/healthcheck.sh`](scripts/healthcheck.sh).
- **Zadatak `lab-05`:** cijeli stack se diže s `docker compose up`.

### 6. tjedan — Continuous Integration

- **Na vježbama:** GitHub Actions — lint, testovi, build imagea; namjerno slomljen test da se vidi crveni pipeline.
- **Kod:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
- **Zadatak `lab-06`:** build imagea u CI-ju na svaki PR.

### 7. tjedan — Continuous Delivery

- **Na vježbama:** push imagea u GHCR na merge u `main`, tagovi `sha` i `latest`, `permissions`; postavljanje taga `checkpoint-1`.
- **Kod:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml); `APP_VERSION` iz [`app/main.py`](app/main.py) dobiva git SHA.
- **Zadatak `lab-07`:** push u GHCR + tag `checkpoint-1` na svom repou.

### 8. tjedan — Infrastructure as Code

- **Otvoreno:** Terraform s kind/helm providerom ili Helm chart. Sadržaj slijedi nakon odluke.
- **Zadatak `lab-08`.**

### 9. tjedan — Configuration management

- **Na vježbama:** Ansible playbook koji instalira ovisnosti i diže stack; drugo pokretanje daje `changed=0`.
- **Kod:** [`infra/ansible/`](infra/ansible/).
- **Zadatak `lab-09`:** idempotentan playbook.

### 10. tjedan — Kubernetes I

- **Na vježbama:** manifesti za shortener — Deployment, Service, ConfigMap, Secret, probe, resources; debugging s `kubectl describe` i `kubectl logs`. Troubleshooting postupak iz 2. tjedna, samo s `kubectl`.
- **Kod:** [`k8s/`](k8s/), cluster iz [`kind/`](kind/).
- **Zadatak `lab-10`:** aplikacija radi na kind clusteru.

### 11. tjedan — Kubernetes II

- **Na vježbama:** Helm chart iz manifesta, Argo CD `Application`; commit u `helm/` i automatski sync; ručna izmjena na clusteru kao primjer drifta.
- **Kod:** [`helm/`](helm/), [`argocd/`](argocd/); ingress koristi portove iz [`kind/kind-config.yaml`](kind/kind-config.yaml).
- **Zadatak `lab-11`:** Helm chart + Argo CD GitOps.

### 12. tjedan — Observability

- **Na vježbama:** `/metrics` u API-ju, Prometheus, Grafana dashboard, alert na error rate; simulirani val 500-ica. Health check iz 2. tjedna postaje pravi alerting.
- **Kod:** [`monitoring/`](monitoring/), `/metrics` u [`app/`](app/).
- **Zadatak `lab-12`:** dashboard, alert i zapisan SLO.

### 13. tjedan — DevSecOps

- **Na vježbama:** Trivy i gitleaks u pipelineu; namjerno ranjiv base image i procurjeli token da pipeline padne; postavljanje taga `checkpoint-2`.
- **Kod:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml), [`.gitignore`](.gitignore).
- **Zadatak `lab-13`:** security u pipelineu + tag `checkpoint-2` na svom repou.

### 14. tjedan — AI u DevOps praksi

- **Na vježbama:** simulirani incident na demo-appu (npr. Redis pada), troubleshooting uz AI uživo, zajedno pišemo postmortem.
- **Kod:** [`docs/postmortem.md`](docs/postmortem.md), [`docs/ai-log.md`](docs/ai-log.md).
- **Zadatak `lab-14`:** postmortem incidenta na svojoj aplikaciji.

### 15. tjedan — Obrane

- Završna prezentacija i obrana: demo pipelinea od commita do deploya i objašnjenje vlastitog koda.

---

## Pokretanje

```bash
make help   # popis svih naredbi
make run    # API na http://localhost:8000
make test   # testovi
```
