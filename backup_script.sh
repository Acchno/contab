#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_DIR="backups"
SOURCE_FILE="dados.xlsx"
DEST_FILE="${BACKUP_DIR}/dados_backup_${TIMESTAMP}.xlsx"

mkdir -p $BACKUP_DIR
cp $SOURCE_FILE $DEST_FILE

# Remover backups antigos e manter apenas os 10 mais recentes
ls -t $BACKUP_DIR/dados_backup_*.xlsx | sed -e '1,10d' | xargs -d '\n' rm -f
