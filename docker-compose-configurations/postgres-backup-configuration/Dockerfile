# Use a base image with a cron service (e.g., Alpine Linux with cron)
FROM alpine:latest

# Set the arguments expected to be passed in by the docker-compose file
ARG BACKUP_SERVER_USERNAME
ARG BACKUP_SERVER_NAME
ARG BACKUP_SERVER_PORT
ARG BACKUP_REMOTE_PATH

# Turn the ARG into an ENV
ENV BACKUP_SERVER_USERNAME=$BACKUP_SERVER_USERNAME
ENV BACKUP_SERVER_NAME=$BACKUP_SERVER_NAME
ENV BACKUP_SERVER_PORT=$BACKUP_SERVER_PORT
ENV BACKUP_REMOTE_PATH=$BACKUP_REMOTE_PATH

# Install rsync and create a backup directory
RUN apk update && apk add rsync

# Copy your rsync script into the container (replace with your script)
COPY postgress_backup_script.sh /postgress_backup_script.sh

# Add the crontab file to schedule backups
COPY crontab /etc/crontabs/root

# Make the script executable
RUN chmod +x /postgress_backup_script.sh

# Start the cron service
CMD ["crond", "-f"]