#!/usr/bin/env bash
# Provjerava /health endpoint svakog servisa i zapisuje rezultat u log.
# Pokretanje:  ./scripts/healthcheck.sh
# Exit code:   0 = svi servisi rade, 1 = barem jedan ne radi
set -euo pipefail

SERVICES=(
  "api=http://localhost:8000/health"
  # 5. tjedan: ovdje dodajemo ostale servise iz compose.yaml
)
LOG="${LOG:-$HOME/healthcheck.log}"
failed=0

for entry in "${SERVICES[@]}"; do
  name="${entry%%=*}"
  url="${entry#*=}"

  if curl -fsS --max-time 3 "$url" >/dev/null 2>&1; then
    status="OK"
  else
    status="FAIL"
    failed=$((failed + 1))
  fi

  echo "$(date '+%F %T') $name $status" | tee -a "$LOG"
done

exit $(( failed > 0 ))
