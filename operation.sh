#!/bin/bash

"""
Usage: ./operation.sh [backup|deploy]
This script is used to perform operations on the server.
It can be used to backup the database and media files, and to deploy to the server.
Can be automated using CI/CD cron jobs.
"""

source .operation.env
source .env

# Backup directory
COMMON_BACKUP_SUBDIR="$(date +'%Y%m%d')"

mkdir -p "$BACKUP_DIR/$COMMON_BACKUP_SUBDIR"



backup_database() {
    sudo docker exec "$POSTGRES_CONTAINER_NAME" pg_dumpall -U "$POSTGRES_USER"  > "$BACKUP_DIR/$COMMON_BACKUP_SUBDIR/$(date +'%Y%m%d%H%M%S')_postgres_backup.backup"
}

backup_media() {
    sudo docker exec "$MEDIA_CONTAINER_NAME" tar czf - /media/ > "$BACKUP_DIR/$COMMON_BACKUP_SUBDIR/$(date +'%Y%m%d%H%M%S')_media_backup.tar.gz"
}


# Deploy function
deploy() {
    git pull origin master
    sudo docker-compose down
    sudo docker-compose -f docker-compose.prod.yml up -d --build
}

# Check command-line argument
if [ "$1" == "backup" ]; then
    backup_database
    backup_media
    echo "Backup of media and database completed."
elif [ "$1" == "deploy" ]; then
    deploy
    echo "Deployment of server completed."
else
    echo "Usage: $0 [backup|deploy]"
    exit 1
fi

