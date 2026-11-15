#!/usr/bin/env bash
# Provjerava sve servise iz compose.yaml i zapisuje rezultat u log.
# Pokretanje:  ./scripts/healthcheck.sh
# Exit code:   0 = svi servisi rade, 1 = barem jedan ne radi
set -euo pipefail

SERVICES=(
  "api=http://localhost:8000/health"
  "db=docker compose exec -T db pg_isready -h 127.0.0.1 -q"
  "cache=docker compose exec -T cache redis-cli ping"
)
LOG="${LOG:-$HOME/healthcheck.log}"
failed=0

# docker compose traži compose.yaml, a cron ne kreće iz repozitorija.
cd "$(dirname "$0")/.."

for entry in "${SERVICES[@]}"; do
  name="${entry%%=*}"
  check="${entry#*=}"

  # URL provjerava curl, a sve ostalo je naredba koja vraća exit code.
  if [[ $check == http* ]]; then
    check="curl -fsS --max-time 3 $check"
  fi

  if bash -c "$check" >/dev/null 2>&1; then
    status="OK"
  else
    status="FAIL"
    failed=$((failed + 1))
  fi

  echo "$(date '+%F %T') $name $status" | tee -a "$LOG"
done

exit $(( failed > 0 ))
