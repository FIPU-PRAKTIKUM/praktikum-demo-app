# helm/

**Helm chart** tvoje aplikacije. Kad ga napraviš (`helm create <ime>`), manifesti iz `k8s/` prelaze u templateove.

Očekuje se:

- `values.yaml` sa zajedničkim postavkama,
- `values-dev.yaml` i `values-prod.yaml` za razlike između okruženja (broj replika, resursi, tag imagea).
