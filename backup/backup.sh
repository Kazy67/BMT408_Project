#!/bin/bash
BACKUP_DIR="/home/gazi/BMT408_Project/backup"
DATE=$(date +"%Y%m%d_%H%M%S")

sudo docker exec bmt408_project-db-1 pg_dump -U gazi_user gazi_db | gzip > "$BACKUP_DIR/db_backup_$DATE.sql.gz"

find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +7 -exec rm {} \;
