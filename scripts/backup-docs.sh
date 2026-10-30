#!/usr/bin/env bash
# Arhivira mapu docs/ u tar.gz s datumom u imenu i briše arhive starije od 7 dana.
# Pokretanje:  ./scripts/backup-docs.sh
# Exit code:   0 = arhiva je napravljena, 1 = greška (npr. ne postoji docs/)
set -euo pipefail

SRC="${SRC:-docs}"
DEST="${DEST:-$HOME/praktikum-backup}"
KEEP_DAYS="${KEEP_DAYS:-7}"

if [ ! -d "$SRC" ]; then
  echo "GREŠKA: mapa '$SRC' ne postoji — pokreni skriptu iz korijena repozitorija." >&2
  exit 1
fi

mkdir -p "$DEST"
ARCHIVE="$DEST/$(basename "$SRC")-$(date '+%F').tar.gz"
tar -czf "$ARCHIVE" "$SRC"
echo "$(date '+%F %T') backup OK: $ARCHIVE"

find "$DEST" -name '*.tar.gz' -type f -mtime +"$KEEP_DAYS" -print -delete

exit 0
