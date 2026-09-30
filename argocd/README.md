# argocd/

**11. tjedan.** Argo CD `Application` manifest koji pokazuje na Helm chart u ovom repozitoriju.

Argo CD radi **pull**: sam povlači promjene iz GitHuba i imagee iz GHCR-a. Zato mu ne treba nikakav ulazni pristup i radi na tvom laptopu iza bilo kojeg firewalla.

Tok: commit u `helm/` → Argo CD primijeti promjenu → sync na cluster.
