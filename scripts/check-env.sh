#!/usr/bin/env bash
# Provjerava jesu li instalirani svi alati potrebni za kolegij.
set -uo pipefail

TOOLS=(git docker kubectl kind helm argocd ansible trivy python3)
missing=0

for t in "${TOOLS[@]}"; do
  if command -v "$t" >/dev/null 2>&1; then
    printf "  [ok]  %-8s %s\n" "$t" "$("$t" version --client --short 2>/dev/null | head -n1 || "$t" --version 2>/dev/null | head -n1)"
  else
    printf "  [--]  %-8s NIJE INSTALIRAN\n" "$t"
    missing=$((missing + 1))
  fi
done

echo
if docker info >/dev/null 2>&1; then
  echo "  [ok]  Docker daemon radi"
else
  echo "  [--]  Docker daemon ne radi (pokreni Docker Desktop ili provjeri WSL integraciju)"
  missing=$((missing + 1))
fi

echo
if [ "$missing" -eq 0 ]; then
  echo "Sve je spremno."
else
  echo "Nedostaje $missing stavki. Pogledaj upute u materijalima kolegija (setup/)."
  exit 1
fi
