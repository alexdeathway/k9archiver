#!/bin/bash

"""
Usage: ./operation.sh [backup|deploy]
This script is used to perform operations on the server.
It can be used to backup/restore the database and media files, and to deploy to the server.
Can be automated using CI/CD cron jobs.
"""
 #for container name and other variables
source .operation.env
#environment variables are needed for incase you need to backup the database with pg_dumpall
source .env 

#this make sure that the backup of same day and are not misplaced
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

elif [ "$1" == "backup_media" ]; then
    backup_media
    echo "Deployment of server completed."

elif [ "$1" == "backup_database" ]; then
    backup_database
    echo "Backup of database completed."



elif [ "$1" == "deploy" ]; then
    deploy
    echo "Deployment to server completed."

elif [ "$1" == "backup_and_deploy" ]; then
    backup_database
    backup_media
    deploy
    echo "Backup and deployment to server completed."


else
    echo "Invalid argument."
    echo "Usage: $0 [backup|backup_media|backup_database|deploy|backup_and_deploy]"
    exit 1
fi

