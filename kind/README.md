# kind/

Konfiguracija lokalnog Kubernetes clustera. **kind** (Kubernetes IN Docker) pokreće cijeli cluster kao Docker kontejnere na tvom računalu. Nema clouda, računa ni kartice, a cluster se diže za minutu i briše bez traga.

Cluster koristimo od 10. tjedna, ali ga podižemo već u 1. tjednu da provjerimo radi li okruženje.

```bash
make cluster-up     # kind create cluster --config kind/kind-config.yaml
kubectl get nodes   # trebao bi se vidjeti jedan node u stanju Ready
make cluster-down   # kind delete cluster --name praktikum
```

## `kind-config.yaml` linija po liniju

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: praktikum
```

Svaki Kubernetes-stil YAML počinje s `kind` (koja vrsta objekta) i `apiVersion` (koja verzija sheme). Taj isti obrazac vidjet ćemo u svakom manifestu u 10. tjednu. `name` je ime clustera; `kubectl` context se zove `kind-praktikum`.

```yaml
nodes:
  - role: control-plane
```

Cluster ima jedan node koji je istovremeno control plane (mozak clustera: API server, scheduler) i worker (na njemu se vrte naše aplikacije). U produkciji su to odvojeni strojevi, a za učenje je jedan dovoljan.

```yaml
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
```

Nodeu dodajemo label `ingress-ready=true`. Ingress controller koji instaliramo u 11. tjednu traži node s tim labelom da bi se na njemu pokrenuo.

```yaml
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
      - containerPort: 443
        hostPort: 443
```

Node je Docker kontejner, pa njegovi portovi nisu automatski dostupni s tvog računala. Ovo povezuje portove 80 i 443 kontejnera s portovima 80 i 443 tvog računala. Zahvaljujući tome u 11. tjednu aplikaciju otvaramo u browseru na `http://localhost`, bez `kubectl port-forward`.

## Česti problemi

| Problem | Uzrok i rješenje |
| --- | --- |
| `Cannot connect to the Docker daemon` | Docker Desktop nije pokrenut, ili na Windowsu nije uključena WSL integracija |
| `port 80 is already in use` | nešto drugo koristi port 80 (često IIS ili Skype na Windowsu, ili lokalni nginx); ugasi ga ili privremeno makni `extraPortMappings` |
| `node(s) already exist for a cluster with the name "praktikum"` | cluster već postoji; `make cluster-down` pa ponovno `make cluster-up` |
| cluster je spor ili se ruši | Dockeru treba barem 4 GB RAM-a. **Windows (WSL2):** memoriju određuje WSL, po defaultu pola RAM-a računala; za više u `%UserProfile%\.wslconfig` upiši `[wsl2]` i `memory=6GB`, pa u PowerShellu `wsl --shutdown`. **macOS:** Docker Desktop → Settings → Resources → Memory |
