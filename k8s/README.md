# k8s/

**10. tjedan.** Kubernetes manifesti za tvoju aplikaciju: `Deployment`, `Service`, `ConfigMap`, `Secret` za svaki servis.

Deploy na lokalni cluster:

```bash
make cluster-up
kubectl apply -f k8s/
kubectl get pods
```

Svaki Deployment mora imati `livenessProbe` i `readinessProbe` na `/health` te postavljene `resources.requests` i `limits`. Secrete ne commitaj u plain textu.
