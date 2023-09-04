#!/bin/sh

# Set the path to the backup target path as a variable for easier use
BACKUP_TARGET_PATH=/backup_source/backup_$(date +%Y-%m-%d_%H-%M-%S).tar.gz

# Create a gzipped tarball of the backup source including the current timestamp as part of the filename
tar --keep-old-files\
    --create\
    --gzip\
    --file=${BACKUP_TARGET_PATH}\
    /backup_source

# Perform the backup using rsync
rsync -avz -e "ssh -p ${BACKUP_SERVER_PORT} -i /run/secrets/postgres_database_backup_ssh_private_key" ${BACKUP_TARGET_PATH} ${BACKUP_SERVER_USERNAME}@${BACKUP_SERVER_NAME}:/${BACKUP_REMOTE_PATH}/
