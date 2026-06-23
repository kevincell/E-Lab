#!/bin/bash
set -euo pipefail

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=${BACKUP_DIR:-/opt/backups/elab}
MEDIA_DIR=${MEDIA_DIR:-/opt/elab/media}
DB_CONTAINER=${DB_CONTAINER:-elab-db}
POSTGRES_USER=${POSTGRES_USER:-elab}
POSTGRES_DB=${POSTGRES_DB:-elab_db}

mkdir -p "$BACKUP_DIR"

docker exec "$DB_CONTAINER" pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_DIR/db_$DATE.sql"
tar czf "$BACKUP_DIR/media_$DATE.tar.gz" "$MEDIA_DIR"

find "$BACKUP_DIR" -name "db_*.sql" -type f -printf "%T@ %p\n" | sort -nr | tail -n +8 | cut -d" " -f2- | xargs -r rm -f
find "$BACKUP_DIR" -name "media_*.tar.gz" -type f -printf "%T@ %p\n" | sort -nr | tail -n +8 | cut -d" " -f2- | xargs -r rm -f
